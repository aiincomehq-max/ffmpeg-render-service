#!/usr/bin/env python3
"""Screen a ClickBank marketplace export against the Product Mastery gates.

Implements Gates 1 (proof of life), 3 (unit economics) and 4 (funnel/trust) from
FRAMEWORK.md. Gate 2 (momentum) needs a time series -- use --snapshot to start
building one, and --compare once you have two dated snapshots. Gate 5
(saturation) is manual.

Input: CSV or JSON export from the ClickBank marketplace / REST API. Field names
vary by export route, so common aliases are normalised.

Usage:
    python3 screen.py marketplace.csv --cpc 0.25 --channel native
    python3 screen.py marketplace.csv --snapshot snapshots/
    python3 screen.py --compare snapshots/2026-09-20.json snapshots/2026-10-18.json

No dependencies beyond the standard library. Nothing here is copied from the
paid product; see FRAMEWORK.md for how the criteria were derived.
"""

import argparse
import csv
import datetime as dt
import json
import os
import re
import sys

# --- thresholds (FRAMEWORK.md section 2) ------------------------------------

# Gravity bands corrected against the Product Mastery guide (p.7 table, p.10).
# It puts the "sweet spot" at mid-double to low-triple digits, and for cold PAID
# traffic says higher is better (150+). The original 8-60 band here would have
# rejected exactly the offers it recommends for paid. Free/warm traffic wants a
# lower band, because the priority there is brand fit, not day-0 profit.
# CORRECTION (2026-10-11, live marketplace pull): absolute gravity thresholds
# are unsafe. The whole marketplace tops out at ~146 today, so ClickBank's own
# "100+ for paid" captures the 3 most-contested offers out of 1,242 -- the exact
# crowding their guide elsewhere says to avoid. The scale has compressed since
# the course was recorded (offers at 300+ were cited not long ago). What the
# advice means is a PERCENTILE, not a number: proven, not top-of-market.
# Re-derive these from the max gravity in each pull rather than trusting them.
GRAVITY_BAND = {
    "paid": (40.0, 110.0),    # roughly ranks 4-31 of 1,242 in the 2026-10 pull
    "free": (10.0, 50.0),
}
PAID_PAYOUT_HINT = 100.0   # p.7: cold paid traffic wants $100+/sale. Soft flag,
                           # not a gate -- the EPC/CPC margin still decides.
REFUND_MAX = 0.15          # 15% on a 30/90-day basis
MARGIN_MIN = 1.5           # required expected-EPC to CPC ratio
USD_PER_GBP = 1.27         # override with --fx

# planning CPC bands in GBP (assumptions, not measurements)
CHANNEL_CPC = {
    "native": (0.05, 0.40),
    "tiktok": (0.30, 0.80),
    "meta": (0.40, 1.20),
    "google": (0.80, 3.00),
}

# --- field normalisation ----------------------------------------------------

ALIASES = {
    "site": ["site", "vendor", "nickname", "vendorNickname", "hopName"],
    "title": ["title", "name", "product", "productTitle", "description"],
    "category": ["category", "categoryName", "primaryCategory"],
    "gravity": ["gravity", "grav", "activityScore", "popularityScore"],
    "commission": [
        "commission", "initialDollarsPerSale", "initial_dollars_per_sale",
        "initialEarningsPerSale", "avgSale", "initial$/sale", "initial $/sale",
    ],
    "avg_sale": [
        "avgAmountPerSale", "avg_amount_per_sale", "averageDollarsPerSale",
        "avg$/sale", "avg $/sale", "avgRebill",
    ],
    "epc": ["average_epc", "averageEpc", "epc", "avgEpc"],
    "cvr": ["cvr", "conversionRate", "conversion_rate", "percentPerSale"],
    "refund": [
        "expectedReturnRate", "expected_return_rate", "returnRate",
        "refundRate", "rebillAmt",
    ],
    "refund_basis": [
        "expectedReturnRateBasis", "expected_return_rate_basis",
        "returnRateBasis", "refundBasis",
    ],
    "recurring": ["recurringCommission", "futureDollarsPerSale", "rebill"],
    "has_affiliate_page": ["hasAffiliateTools", "affiliatePage", "affiliateToolsUrl"],
}

# ClickBank sometimes reports these as a 0-100 number rather than a 0-1 fraction.
_PERCENTISH = ("cvr", "refund")


def _norm_key(k):
    return re.sub(r"[^a-z0-9]", "", str(k).lower())


def _lookup(row, field):
    wanted = {_norm_key(a) for a in ALIASES[field]}
    for k, v in row.items():
        if _norm_key(k) in wanted:
            return v
    return None


def _num(v):
    """Parse a number out of '$102.01', '3.89%', '1,234' or ''."""
    if v is None:
        return None
    if isinstance(v, (int, float)):
        return float(v)
    s = str(v).strip().replace(",", "").replace("$", "").replace("%", "")
    if not s or s.lower() in ("n/a", "na", "none", "-"):
        return None
    try:
        return float(s)
    except ValueError:
        return None


def normalise(row):
    out = {}
    for field in ALIASES:
        raw = _lookup(row, field)
        if field in ("site", "title", "category", "refund_basis"):
            out[field] = str(raw).strip() if raw not in (None, "") else ""
        else:
            out[field] = _num(raw)
    for field in _PERCENTISH:
        v = out.get(field)
        if v is not None and v > 1.0:
            out[field] = v / 100.0
    return out


# --- gates ------------------------------------------------------------------

def gate1_proof_of_life(p, traffic):
    lo, hi = GRAVITY_BAND[traffic]
    g = p["gravity"]
    if g is None:
        return False, "no gravity reported"
    if g < lo:
        return False, f"gravity {g:.1f} < {lo:.0f} (too few affiliates earning)"
    if g > hi:
        return False, f"gravity {g:.1f} > {hi:.0f} (saturated end)"
    if not p["commission"]:
        return False, "no commission reported"
    note = f"gravity {g:.1f}"
    if traffic == "paid" and p["commission"] < PAID_PAYOUT_HINT:
        note += f" | payout ${p['commission']:.0f} under the ${PAID_PAYOUT_HINT:.0f} cold-paid hint"
    return True, note


def gate4_trust(p):
    r, basis = p["refund"], (p["refund_basis"] or "").lower()
    if r is None:
        return "unknown", "no return rate reported"
    if "categor" in basis or not basis:
        # vendor has no own history: unknown, not a rejection (FRAMEWORK 2, Gate 4)
        return "unknown", f"return rate {r:.1%} on category-average basis (vendor has no history)"
    if r > REFUND_MAX:
        return False, f"return rate {r:.1%} > {REFUND_MAX:.0%} ({basis})"
    return True, f"return rate {r:.1%} ({basis})"


def gate3_economics(p, cpc_gbp, fx):
    """Expected EPC in GBP vs planning CPC. Returns (pass, detail, margin)."""
    c = p["commission"]
    cvr = p["cvr"]
    if c is None or cvr is None:
        return "unknown", "commission or CVR missing -- cannot compute EPC", None
    r = p["refund"] if p["refund"] is not None else 0.0
    net_usd = c * (1.0 - r)
    epc_gbp = (cvr * net_usd) / fx
    margin = epc_gbp / cpc_gbp if cpc_gbp else float("inf")
    detail = (f"net ${net_usd:.2f} x CVR {cvr:.2%} = EPC £{epc_gbp:.2f} "
              f"vs CPC £{cpc_gbp:.2f} -> {margin:.1f}x")
    return (margin >= MARGIN_MIN), detail, margin


def verdict(p, cpc_gbp, fx, traffic):
    reasons = []
    ok1, d1 = gate1_proof_of_life(p, traffic)
    reasons.append(("G1", ok1, d1))
    if not ok1:
        return "REJECT", reasons, None

    ok3, d3, margin = gate3_economics(p, cpc_gbp, fx)
    reasons.append(("G3", ok3, d3))
    if ok3 is False:
        return "REJECT", reasons, margin

    ok4, d4 = gate4_trust(p)
    reasons.append(("G4", ok4, d4))
    if ok4 is False:
        return "REJECT", reasons, margin

    # Gate 2 is always unknown from a single snapshot, so nothing reaches TEST
    # on data alone -- that is the point, not a bug.
    if ok3 == "unknown" or ok4 == "unknown":
        return "WATCH", reasons, margin
    return "WATCH*", reasons, margin


# --- io ---------------------------------------------------------------------

def load(path):
    with open(path, newline="", encoding="utf-8-sig") as fh:
        head = fh.read(2048)
        fh.seek(0)
        if head.lstrip().startswith(("{", "[")):
            data = json.load(fh)
            if isinstance(data, dict):
                for key in ("products", "items", "results", "data"):
                    if isinstance(data.get(key), list):
                        data = data[key]
                        break
                else:
                    data = [data]
            return data
        try:
            dialect = csv.Sniffer().sniff(head)
        except csv.Error:
            dialect = csv.excel
        return list(csv.DictReader(fh, dialect=dialect))


def cmd_screen(args):
    lo, hi = CHANNEL_CPC[args.channel]
    cpc = args.cpc if args.cpc is not None else (lo + hi) / 2
    rows = [normalise(r) for r in load(args.input)]

    scored = []
    for p in rows:
        v, reasons, margin = verdict(p, cpc, args.fx, args.traffic)
        scored.append((v, margin if margin is not None else -1, p, reasons))

    rank = {"WATCH*": 0, "WATCH": 1, "REJECT": 2}
    scored.sort(key=lambda t: (rank.get(t[0], 3), -t[1]))

    print(f"\nChannel: {args.channel}  planning CPC £{cpc:.2f} "
          f"(band £{lo:.2f}-£{hi:.2f})   FX ${args.fx}/£")
    glo, ghi = GRAVITY_BAND[args.traffic]
    print(f"Gates: G1 gravity {glo:.0f}-{ghi:.0f} ({args.traffic} traffic) | "
          f"G3 EPC >= {MARGIN_MIN}x CPC | G4 refunds < {REFUND_MAX:.0%}")
    print("G2 (momentum) needs a time series -- see --snapshot. "
          "Nothing is TEST-rated until G2 and G5 are done by hand.\n")

    shown = 0
    for v, margin, p, reasons in scored:
        if v == "REJECT" and not args.show_rejects:
            continue
        if args.limit and shown >= args.limit and v != "REJECT":
            break
        name = p["title"] or p["site"] or "?"
        print(f"[{v:7}] {name[:58]:58} {p['category'][:22]:22}")
        for tag, ok, detail in reasons:
            mark = {True: "pass", False: "FAIL", "unknown": "????"}[ok]
            print(f"           {tag} {mark}  {detail}")
        print()
        shown += 1

    counts = {}
    for v, _, _, _ in scored:
        counts[v] = counts.get(v, 0) + 1
    print("Totals: " + "  ".join(f"{k}={v}" for k, v in sorted(counts.items())))
    print(f"\nNext: take the top {min(10, shown) or 10} into Gate 5 "
          f"(Meta Ad Library / TikTok / Google 'review' SERP / Reddit).")


def cmd_snapshot(args):
    os.makedirs(args.snapshot, exist_ok=True)
    rows = [normalise(r) for r in load(args.input)]
    keep = [{"site": p["site"], "title": p["title"], "category": p["category"],
             "gravity": p["gravity"], "commission": p["commission"],
             "cvr": p["cvr"], "refund": p["refund"]} for p in rows]
    stamp = dt.date.today().isoformat()
    out = os.path.join(args.snapshot, f"{stamp}.json")
    with open(out, "w", encoding="utf-8") as fh:
        json.dump({"date": stamp, "products": keep}, fh, indent=1)
    print(f"Wrote {len(keep)} products to {out}")
    print("Repeat weekly. Two or more snapshots enable --compare (Gate 2).")


def cmd_compare(args):
    old_path, new_path = args.compare
    def index(path):
        with open(path, encoding="utf-8") as fh:
            d = json.load(fh)
        return d.get("date", path), {
            (p.get("site"), p.get("title")): p for p in d["products"]}

    d_old, old = index(old_path)
    d_new, new = index(new_path)
    moves = []
    for key, p in new.items():
        prev = old.get(key)
        g_new = p.get("gravity")
        if g_new is None:
            continue
        if prev is None:
            moves.append((float("inf"), p, None, "NEW to marketplace"))
            continue
        g_old = prev.get("gravity")
        if not g_old:
            continue
        ratio = g_new / g_old
        moves.append((ratio, p, g_old,
                      f"{g_old:.1f} -> {g_new:.1f}  ({ratio - 1:+.0%})"))

    moves.sort(key=lambda t: -t[0])
    print(f"\nGate 2 momentum: {d_old} -> {d_new}   (rising = ratio >= 1.25)\n")
    for ratio, p, _, detail in moves[:args.limit or 25]:
        flag = "RISING" if ratio >= 1.25 else ("new   " if ratio == float("inf") else "      ")
        print(f"[{flag}] {(p.get('title') or p.get('site') or '?')[:52]:52} {detail}")
    n = sum(1 for r, *_ in moves if r >= 1.25)
    print(f"\n{n} offer{'' if n == 1 else 's'} rising. "
          f"Cross these against the WATCH* list from the screen run.")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("input", nargs="?", help="marketplace export (CSV or JSON)")
    ap.add_argument("--channel", choices=sorted(CHANNEL_CPC), default="native")
    ap.add_argument("--traffic", choices=sorted(GRAVITY_BAND), default="paid",
                    help="selects the gravity band (Product Mastery p.7 table)")
    ap.add_argument("--cpc", type=float, help="planning CPC in GBP (default: channel midpoint)")
    ap.add_argument("--fx", type=float, default=USD_PER_GBP, help="USD per GBP")
    ap.add_argument("--limit", type=int, default=15)
    ap.add_argument("--show-rejects", action="store_true")
    ap.add_argument("--snapshot", metavar="DIR", help="write a dated snapshot for Gate 2")
    ap.add_argument("--compare", nargs=2, metavar=("OLD", "NEW"),
                    help="compare two snapshots for momentum")
    args = ap.parse_args()

    if args.compare:
        return cmd_compare(args)
    if not args.input:
        ap.error("an input export is required (or use --compare)")
    if args.snapshot:
        return cmd_snapshot(args)
    return cmd_screen(args)


if __name__ == "__main__":
    sys.exit(main() or 0)
