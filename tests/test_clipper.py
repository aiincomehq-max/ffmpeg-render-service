"""Fast safety-net tests (no network, no API keys).

    python -m unittest discover -s tests -v
    RUN_RENDER=1 python -m unittest discover -s tests -v    # also renders a real video (~1 min)
"""
import datetime as dt
import json
import os
import random
import shutil
import sys
import unittest
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
os.environ["CLIPPER_DRY_RUN"] = "1"

from clipper import ass as A  # noqa: E402
from clipper import channels, edl as E, moments, performance, publish, scout, track  # noqa: E402
from clipper.style import load  # noqa: E402

STYLE = load()


def words(start, end, step=0.35, gaps=()):
    out, t = [], start
    while t < end:
        if any(a <= t < b for a, b in gaps):
            t += 0.1
            continue
        out.append({"w": "bro", "s": round(t, 2), "e": round(t + 0.28, 2)})
        t += step
    return out


def tmp_channel(name="speed"):
    ch = channels.get(name)
    ch["key"] = f"_test_{uuid.uuid4().hex[:6]}"
    return ch


class TestEDL(unittest.TestCase):
    def test_long_silence_cut_but_payoff_protected(self):
        m = {"src": "x", "start": 0, "end": 30, "payoff_t": 20.5,
             "words": words(0, 30, gaps=[(5, 9), (19, 22)])}
        kept = E._speech_ranges(m)
        covered = lambda t: any(a <= t <= b for a, b in kept)
        self.assertFalse(covered(7.0), "4s silence should be cut")
        self.assertTrue(covered(20.5), "silence around the payoff must be kept")

    def test_single_moment_shape(self):
        m = {"src": "x", "start": 10, "end": 90, "payoff_t": 60, "hook_tag": "HOOK", "emoji": "💀",
             "words": words(10, 90), "action_tags": [{"t": 40, "text": "WAIT FOR IT"}]}
        e = E.single_moment(m, STYLE, "@h", None)
        dur = sum((p["end"] - p["start"]) / p["speed"] for p in e["pieces"])
        self.assertLessEqual(dur, E.MAX_LEN + 0.01)
        self.assertEqual(e["format"], "single_moment")
        self.assertTrue(any(i.get("emoji") == "💀" for i in e["impacts"]))
        self.assertTrue(all(w["s"] <= dur for w in e["words"]))
        self.assertEqual(e["texts"][0]["start"], 0.0)

    def test_wholesome_variant(self):
        m = {"src": "x", "start": 0, "end": 30, "payoff_t": 25, "type": "wholesome", "comedic": True,
             "emoji": "😭", "words": words(0, 30)}
        e = E.single_moment(m, STYLE, "@h", "music.wav")
        self.assertEqual(e["format"], "wholesome_fan")
        self.assertIsNone(e["end_sfx"])
        self.assertTrue(all(i["flash"] is None and i["sfx"] is None for i in e["impacts"]))

    def test_subversion_comp_length_and_header(self):
        fail = {"src": "x", "start": 0, "end": 6, "payoff_t": 3}
        wins = [{"src": "x", "start": 10 + i * 10, "end": 18 + i * 10, "impact_ts": [14 + i * 10]} for i in range(5)]
        e = E.subversion_comp("cant dance", fail, wins, STYLE, "@h", None, name="Kai")
        dur = sum((p["end"] - p["start"]) / p["speed"] for p in e["pieces"])
        self.assertTrue(18 <= dur <= 24, dur)
        self.assertIn("KAI CANT DANCE", e["texts"][0]["text"])
        self.assertEqual(sum(1 for p in e["pieces"] if p["speed"] < 1), 5)


class TestASS(unittest.TestCase):
    def test_colour_and_groups(self):
        self.assertEqual(A.ass_color("#FFD700"), "&H0000D7FF")
        g = A.group_words([{"w": "a", "s": 0, "e": 0.2}, {"w": "b", "s": 0.3, "e": 0.5},
                           {"w": "c", "s": 0.6, "e": 0.8}, {"w": "d", "s": 0.9, "e": 1.0},
                           {"w": "e", "s": 3.0, "e": 3.2}])
        self.assertEqual([len(x) for x in g], [3, 1, 1])


class TestScout(unittest.TestCase):
    def test_heatmap_peaks(self):
        dur = 3600
        hm = [{"start_time": i * 36, "end_time": i * 36 + 36, "value": 0.1} for i in range(100)]
        hm[0]["value"] = 1.0          # intro spike: must be ignored
        hm[30]["value"] = 0.9
        hm[31]["value"] = 0.85        # same peak area: must merge
        hm[70]["value"] = 0.6
        secs = scout.heatmap_sections(hm, dur, 5)
        mids = [(s + e) / 2 for s, e, _ in secs]
        self.assertFalse(any(m < 100 for m in mids), "intro spike picked")
        self.assertEqual(len([m for m in mids if 900 < m < 1300]), 1, "nearby peaks not merged")
        self.assertTrue(any(2400 < m < 2700 for m in mids))
        self.assertEqual(scout.fmt(3725), "01:02:05")


class TestTrack(unittest.TestCase):
    def test_deadzone_holds_then_follows(self):
        samples = [(i * 0.2, 0.50 + (0.01 if i % 2 else 0)) for i in range(10)] + \
                  [(2 + i * 0.2, 0.80) for i in range(15)]
        path = track.smooth_path(samples)
        self.assertAlmostEqual(path[5][1], path[0][1], places=3)   # jitter ignored
        self.assertGreater(path[-1][1], 0.70)                       # big move followed
        self.assertIsNone(track.smooth_path([(0, None), (0.2, None)]))


class TestMoments(unittest.TestCase):
    def test_prompts_render_for_every_channel(self):
        for key in channels.load_all():
            s = moments._system(channels.get(key))
            self.assertNotIn("{streamer", s)
            self.assertNotIn("{short", s)

    def test_dedupe_and_windows(self):
        d = moments._dedupe([{"start": 0, "end": 30, "virality": 8}, {"start": 5, "end": 32, "virality": 9},
                             {"start": 40, "end": 60, "virality": 7}])
        self.assertEqual([m["virality"] for m in d], [9, 7])
        segs = [{"s": i * 5.0, "e": i * 5 + 4, "text": "x"} for i in range(300)]
        self.assertGreaterEqual(len(moments._windows(segs)), 3)

    def test_schema_strict(self):
        sc = moments._schema(["reflexes"])
        item = sc["properties"]["moments"]["items"]
        self.assertFalse(item["additionalProperties"])
        self.assertEqual(set(item["required"]), set(item["properties"]))


class TestPublish(unittest.TestCase):
    def setUp(self):
        self.ch = tmp_channel()
        self.day = ROOT / "out" / self.ch["key"] / "2026-01-01"
        self.day.mkdir(parents=True)
        for i in range(3):
            (self.day / f"v{i}.mp4").write_bytes(b"0")

    def tearDown(self):
        shutil.rmtree(ROOT / "out" / self.ch["key"], ignore_errors=True)
        shutil.rmtree(ROOT / "data" / self.ch["key"], ignore_errors=True)

    def test_slots_spread_and_idempotent(self):
        posts = [{"file": f"v{i}.mp4", "titles": [f"t{i}"], "format": "single_moment"} for i in range(3)]
        slots = [publish.approve(self.ch, self.day, p, p["titles"][0], ["youtube", "tiktok"])["slot"] for p in posts]
        self.assertEqual(len(set(slots)), 3, "each approval should get its own slot")
        self.assertEqual(slots, sorted(slots))
        again = publish.approve(self.ch, self.day, posts[0], "other", ["youtube"])
        self.assertEqual(again["slot"], slots[0], "re-approving must not post twice")
        st = publish.load_state(self.ch)
        self.assertEqual(st["2026-01-01/v0.mp4"]["meta"]["format"], "single_moment")

    def test_slot_times_are_configured_utc(self):
        now = dt.datetime(2026, 1, 1, 15, 0, tzinfo=dt.timezone.utc)
        s = publish.next_slot(self.ch, {}, now)
        self.assertEqual((s.hour, s.minute), (16, 45))

    def test_platform_payloads(self):
        yt = publish.blotato.target("youtube", "x" * 150)
        self.assertEqual(len(yt["title"]), 100)
        self.assertFalse(yt["isMadeForKids"])
        tt = publish.blotato.target("tiktok", "t")
        self.assertEqual(tt["privacyLevel"], "PUBLIC_TO_EVERYONE")
        self.assertEqual(publish.blotato.target("instagram", "t")["mediaType"], "reel")


class TestLearningLoop(unittest.TestCase):
    """Simulates 10 posted Shorts, fake views after 48h, and checks learnings feed the prompt."""

    def setUp(self):
        self.ch = tmp_channel()

    def tearDown(self):
        shutil.rmtree(ROOT / "data" / self.ch["key"], ignore_errors=True)

    def test_collect_and_learn(self):
        t0 = dt.datetime(2026, 1, 1, 14, 0, tzinfo=dt.timezone.utc)
        rng = random.Random(1)
        st = {}
        for i in range(10):
            wholesome = i % 2 == 0
            st[f"d/v{i}.mp4"] = {
                "status": "scheduled", "utc": t0.strftime("%Y-%m-%dT%H:%M:%SZ"), "title": f"Title {i}",
                "platforms": {"youtube": f"pid{i}", "tiktok": "dry-x"},
                "meta": {"format": "wholesome_fan" if wholesome else "single_moment",
                         "type": "wholesome" if wholesome else "funny", "virality": 9 if wholesome else 7,
                         "duration": 45 if wholesome else 20, "hook_tag": f"HOOK {i}"}}
        publish.save_state(self.ch, st)
        fake_status = lambda pid: {"publicUrl": f"https://youtube.com/shorts/{pid}"}
        fake_fetch = lambda url: {"views": (500_000 if int(url[-1]) % 2 == 0 else 20_000) + rng.randint(0, 999),
                                  "likes": 1, "comments": 0}
        # too early: nothing measured
        self.assertEqual(performance.collect(self.ch, fake_fetch, fake_status, t0 + dt.timedelta(hours=10)), 0)
        n = performance.collect(self.ch, fake_fetch, fake_status, t0 + dt.timedelta(hours=50))
        self.assertEqual(n, 10)  # youtube only; dry-run tiktok ids skipped
        # same checkpoint again: no duplicate measurement
        self.assertEqual(performance.collect(self.ch, fake_fetch, fake_status, t0 + dt.timedelta(hours=60)), 0)
        txt = performance.write_learnings(self.ch)
        self.assertIn("Top performers", txt)
        top_line = txt.splitlines()[2]
        self.assertIn("wholesome", top_line)
        self.assertIn("Calibration", txt)
        self.assertIn("YOUR CHANNEL'S OWN RESULTS", moments._system(self.ch))


@unittest.skipUnless(os.environ.get("RUN_RENDER") == "1", "set RUN_RENDER=1 for the slow render test")
class TestRender(unittest.TestCase):
    def test_render_end_to_end(self):
        import subprocess
        from clipper.render import probe_duration, render
        work = ROOT / "out" / "_test_render"
        work.mkdir(parents=True, exist_ok=True)
        src = work / "src.mp4"
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "lavfi", "-i", "testsrc2=size=1920x1080:rate=30:duration=20",
                        "-f", "lavfi", "-i", "sine=duration=20", "-c:v", "libx264", "-preset", "ultrafast",
                        "-c:a", "aac", "-shortest", str(src)], check=True)
        m = {"src": str(src), "start": 1, "end": 15, "payoff_t": 12, "hook_tag": "TEST", "emoji": "💀",
             "words": words(1, 15)}
        out = render(E.single_moment(m, STYLE, "@h", None), STYLE, work / "o.mp4")
        self.assertTrue(10 < probe_duration(str(out)) < 15)
        shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    unittest.main()
