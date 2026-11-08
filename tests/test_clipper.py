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


class TestLiveServiceFixes(unittest.TestCase):
    def test_ytdlp_ignores_user_config(self):
        # a user's ~/.config/yt-dlp/config (e.g. an unquoted --output with spaces) must not break us
        import subprocess as sp
        from unittest import mock
        seen = []

        def fake_run(cmd, **kw):
            seen.append(cmd)
            return sp.CompletedProcess(cmd, 0, stdout='{"id": "x", "entries": []}', stderr="")
        with mock.patch("subprocess.run", fake_run):
            scout.latest_streams("https://www.youtube.com/@x/streams")
            scout.stream_peaks("https://www.youtube.com/watch?v=x")
            from clipper import ingest
            ingest.info("https://www.youtube.com/watch?v=x")
            import tempfile
            with mock.patch.object(ingest, "VODS", Path(tempfile.mkdtemp())):
                ingest.download_audio("https://www.youtube.com/watch?v=x", {"id": "x"})
        self.assertTrue(seen and all(c[0] == "yt-dlp" and "--ignore-config" in c for c in seen))

    def test_load_wav_without_pyav(self):
        import tempfile
        import wave
        import numpy as np
        from clipper.transcribe import load_wav
        with tempfile.TemporaryDirectory() as d:
            f = Path(d, "a.wav")
            with wave.open(str(f), "wb") as w:
                w.setnchannels(1), w.setsampwidth(2), w.setframerate(16000)
                w.writeframes(np.array([0, 16384, -32768], dtype="<i2").tobytes())
            a = load_wav(f)
        self.assertEqual(a.dtype, np.float32)
        self.assertEqual(a.tolist(), [0.0, 0.5, -1.0])

    def test_captions_never_overlap(self):
        # last word of a group is held >=0.25s; it must not run into the next group (seen as "TYOU THANK YOUK")
        import re
        ws = [{"w": "thank", "s": 1.0, "e": 1.1}, {"w": "you.", "s": 1.12, "e": 1.15},
              {"w": "thank", "s": 1.2, "e": 1.3}, {"w": "you", "s": 1.3, "e": 1.4}]
        ev = A.caption_events(ws, STYLE, "#00FF00", 60)

        def sec(x):
            h, m, s = x.split(":")
            return int(h) * 3600 + int(m) * 60 + float(s)
        spans = [tuple(sec(x) for x in re.match(r"Dialogue: \d+,([^,]+),([^,]+),", e).groups()) for e in ev]
        for (a0, a1), (b0, b1) in zip(spans, spans[1:]):
            self.assertLessEqual(a1, b0 + 1e-9)
            self.assertLess(a0, a1)

    def test_emoji_moves_off_face(self):
        face = [(440, 1300, 200, 220)]            # face in the lower third, centre
        self.assertEqual(track.clear_x([], 1420, 400, 1080), 540)
        x = track.clear_x(face, 1420, 400, 1080)
        self.assertNotEqual(x, 540)
        self.assertFalse(x - 200 < 640 and 440 < x + 200)   # no horizontal overlap with the face box


class TestChannelPlatforms(unittest.TestCase):
    def test_youtube_only_channel(self):
        self.assertEqual(publish.platforms({"platforms": ["youtube"]}), ["youtube"])
        self.assertEqual(publish.platforms({}), publish.PLATFORMS)
        self.assertEqual(channels.get("kai")["platforms"], ["youtube"])


class TestSpendLog(unittest.TestCase):
    def test_log_usage_prices_opus(self):
        import clipper, types
        ch = f"_test_{uuid.uuid4().hex[:6]}"
        resp = types.SimpleNamespace(model="claude-opus-5-5", usage=types.SimpleNamespace(
            input_tokens=1_000_000, output_tokens=100_000, cache_creation_input_tokens=0, cache_read_input_tokens=0))
        try:
            self.assertAlmostEqual(clipper.log_usage(resp, "t", ch), 4.0 + 2.0)
            self.assertTrue((Path(clipper.__file__).parent.parent / "data" / ch / "api_usage.jsonl").exists())
        finally:
            shutil.rmtree(Path(clipper.__file__).parent.parent / "data" / ch, ignore_errors=True)


class TestVisionFloor(unittest.TestCase):
    def test_low_visual_score_is_dropped_even_if_kept(self):
        from clipper import __main__ as M, vision
        old_check, old_mark, env = vision.check, M.library.mark_used, os.environ.get("CLIPPER_VISION")
        scores = {1: 5, 2: 8, 3: None}
        vision.check = lambda m, ch: {"keep": True, "payoff_t": None, "visual_score": scores[m["_id"]], "reason": "x"}
        M.library.mark_used = lambda ids: None
        os.environ["CLIPPER_VISION"] = "1"
        try:
            kept = M.vision_filter([{"_id": 1}, {"_id": 2}, {"_id": 3}], 3)
            self.assertEqual([m["_id"] for m in kept], [2, 3])
            self.assertIn("small corner facecam", open(vision.__file__).read())
        finally:
            vision.check, M.library.mark_used = old_check, old_mark
            if env is None: os.environ.pop("CLIPPER_VISION", None)
            else: os.environ["CLIPPER_VISION"] = env


class TestDiversify(unittest.TestCase):
    """8 Nov: a run picked 4 KFC moments from the scene already posted, plus a twin of a booked Short."""

    def test_stream_pos(self):
        from clipper import library
        self.assertEqual(library.stream_pos("o1_FvfJD8fg_021519021814", 10), ("o1_FvfJD8fg", 2 * 3600 + 15 * 60 + 19 + 10))
        self.assertEqual(library.stream_pos("manualkey", 5), ("manualkey", 5.0))

    def test_same_scene_and_cap_and_legacy_dropped(self):
        from clipper import __main__ as M
        mk = lambda vod, start, kind="fresh": {"_vod": vod, "start": start, "source_kind": kind}
        used = [("A", 2 * 3600 + 11 * 60)]                       # posted: stream A at 2:11:00
        pool = [mk("A_021519021814", 0),                           # 2:15:19 -> same scene as posted
                mk("A_030000030300", 0), mk("A_040000040300", 0), mk("A_050000050300", 0),  # 3 more of A -> cap 2
                mk("B_010000010300", 30), mk("B_010000010300", 90),  # 60 s apart -> same scene, keep first
                {"_vod": "C_000000000300", "start": 0}]              # legacy (no source_kind) -> dropped
        out = M.diversify(pool, used)
        got = [(m["_vod"], m["start"]) for m in out]
        self.assertEqual(got, [("A_030000030300", 0), ("A_040000040300", 0), ("B_010000010300", 30)])


class TestExactSlot(unittest.TestCase):
    def test_approve_at_exact_utc_time(self):
        import tempfile
        tmp = Path(tempfile.mkdtemp()); old = publish.ROOT; env = os.environ.get("CLIPPER_DRY_RUN")
        os.environ["CLIPPER_DRY_RUN"] = "1"; publish.ROOT = tmp
        try:
            ch = {"key": "x", "credit": "c", "hashtags": "#h"}
            when = (dt.datetime.now(dt.timezone.utc) + dt.timedelta(days=2)).replace(hour=14, minute=0, second=0, microsecond=0)
            iso = when.strftime("%Y-%m-%dT%H:%M:%SZ")
            e = publish.approve(ch, tmp, {"file": "a.mp4"}, "t", ["youtube"], when=iso)
            self.assertEqual(e["status"], "scheduled"); self.assertEqual(e["utc"], iso)
            with self.assertRaises(ValueError):
                publish.approve(ch, tmp, {"file": "b.mp4"}, "t", ["youtube"], when="2020-01-01T14:00:00Z")
        finally:
            publish.ROOT = old; shutil.rmtree(tmp, ignore_errors=True)
            if env is None: os.environ.pop("CLIPPER_DRY_RUN", None)
            else: os.environ["CLIPPER_DRY_RUN"] = env


class TestFacebook(unittest.TestCase):
    def test_facebook_post_carries_page_id(self):
        from clipper import blotato
        log = []
        blotato.create_post("facebook", {"account": "31275", "page": "1420386957826930"}, "t", "https://x/v.mp4",
                            "title", None, log)
        body = log[-1]["post"]["post"]
        self.assertEqual(body["accountId"], "31275")
        self.assertEqual(body["target"], {"targetType": "facebook", "pageId": "1420386957826930", "mediaType": "reel"})
        self.assertIn("facebook", publish.PLATFORMS)
        with self.assertRaises(ValueError):
            blotato.create_post("facebook", "31275", "t", "u", "title", None, [])


class TestTwoBatches(unittest.TestCase):
    """Fresh (Claude-estimated, new streams) and heatmap ('Most replayed', weeks later) must coexist."""

    def setUp(self):
        import tempfile
        from clipper import __main__ as M, library
        self.M, self.library = M, library
        self.tmp = Path(tempfile.mkdtemp())
        self._root, self._chan = M.ROOT, library.CHANNEL
        M.ROOT = self.tmp
        library.CHANNEL = f"_test_{uuid.uuid4().hex[:6]}"
        M.CH.clear(); M.CH.update({"key": library.CHANNEL})

    def tearDown(self):
        shutil.rmtree(self.library.db_path().parent, ignore_errors=True)
        shutil.rmtree(self.tmp, ignore_errors=True)
        self.M.ROOT, self.library.CHANNEL = self._root, self._chan

    def test_seen_sets_are_separate(self):
        self.M.mark_seen({"vid1"}, "fresh")
        self.assertIn("vid1", self.M.seen("fresh"))
        self.assertNotIn("vid1", self.M.seen("heatmap"))   # its proven batch must still happen later

    def test_same_moment_not_added_twice_and_kind_filter(self):
        m = {"start": 30.0, "end": 60.0, "payoff_t": 50.0, "type": "funny", "skill": "none", "outcome": "na",
             "virality": 8, "source_kind": "fresh", "video_id": "vid1", "abs_start": 1230.0}
        self.library.add("vid1_a", Path("a.mp4"), [m])
        self.assertTrue(self.library.exists_near("vid1", 1233.0))        # same moment seen via another section
        self.assertFalse(self.library.exists_near("vid1", 1300.0))
        self.assertFalse(self.library.exists_near("vid2", 1230.0))
        h = dict(m, start=5.0, source_kind="heatmap", abs_start=4000.0)
        self.library.add("vid1_b", Path("b.mp4"), [h])
        self.assertEqual([x["source_kind"] for x in self.library.top(None, 5, 7, kind="fresh")], ["fresh"])
        self.assertEqual([x["source_kind"] for x in self.library.top(None, 5, 7, kind="heatmap")], ["heatmap"])

    def test_fresh_windows_pad_and_merge(self):
        ms = [{"start": 100, "end": 130, "virality": 9}, {"start": 150, "end": 170, "virality": 8},
              {"start": 900, "end": 930, "virality": 7}, {"start": 2000, "end": 2030, "virality": 3}]
        w = self.M.fresh_windows(ms, 3000, 3)
        self.assertEqual(w, [(55.0, 190.0), (855.0, 950.0)])   # first two overlap once padded -> merged

    def test_batch_label(self):
        self.assertIn("FRESH", publish.batch_label({"source_kind": "fresh"}))
        self.assertIn("PROVEN", publish.batch_label({"source_kind": "heatmap"}))


class TestHook(unittest.TestCase):
    def test_prompt_bans_empty_teasers(self):
        from clipper.moments import SYSTEM
        self.assertIn("concrete detail", SYSTEM)
        self.assertIn("WAIT FOR HIS REACTION", SYSTEM.split("BANNED")[1])

    def test_hook_text_plain_and_short(self):
        self.assertEqual(E.hook_text("*wait for his first customer* 😭💀"), "WAIT FOR HIS FIRST CUSTOMER")
        self.assertLessEqual(len(E.hook_text("NO WAY HE DID THIS AT THE END OF THE STREAM TODAY")), 34)

    def test_opening_hook_is_big_and_first(self):
        from clipper import ass
        self.assertIn("Style: Hook,", ass.header(STYLE))
        m = {"start": 10.0, "end": 30.0, "payoff_t": 25.0, "impact_ts": [25.0], "hook_tag": "SPEED WORKS THE KFC DRIVE-THRU",
             "words": words(10.0, 30.0), "action_tags": [{"t": 11.0, "text": "TOO EARLY"}, {"t": 20.0, "text": "WAIT"}],
             "src": "x.mp4", "type": "funny"}
        edl = E.single_moment(m, STYLE, "TURBOCLIPZ", None)
        hook = [t for t in edl["texts"] if t["kind"] == "hook"]
        self.assertEqual(len(hook), 1)
        self.assertEqual(hook[0]["start"], 0.0)
        self.assertEqual(hook[0]["text"], "SPEED WORKS THE KFC DRIVE-THRU")
        # no action tag fights the hook on screen
        self.assertTrue(all(t["start"] >= hook[0]["end"] for t in edl["texts"] if t["kind"] != "hook"))

    def test_burned_captions_skip_ours_and_tags_drop_emoji(self):
        m = {"start": 10.0, "end": 30.0, "payoff_t": 25.0, "impact_ts": [25.0], "hook_tag": "KAI ASKED HIS NAME",
             "words": words(10.0, 30.0), "action_tags": [{"t": 20.0, "text": "HE WENT OFF 🤬"}],
             "src": "x.mp4", "type": "funny"}
        self.assertTrue(E.single_moment(m, STYLE, "R", None)["words"])
        edl = E.single_moment(dict(m, burned_captions=True), STYLE, "R", None)
        self.assertEqual(edl["words"], [])
        self.assertIn("*HE WENT OFF*", [t["text"] for t in edl["texts"]])


class TestFFmpegPath(unittest.TestCase):
    def test_prefers_full_build(self):
        import tempfile
        from clipper import prefer_full_ffmpeg
        with tempfile.TemporaryDirectory() as d:
            Path(d, "ffmpeg").write_text("")
            env = {"PATH": "/usr/bin"}
            self.assertEqual(prefer_full_ffmpeg((d,), env), d)
            self.assertTrue(env["PATH"].startswith(d + os.pathsep))
            prefer_full_ffmpeg((d,), env)
            self.assertEqual(env["PATH"].count(d), 1)
            self.assertIsNone(prefer_full_ffmpeg(("/nonexistent",), {"PATH": "/usr/bin"}))


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
