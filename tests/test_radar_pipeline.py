"""Contract tests: independent numeric examples and failure behavior."""
import copy
import json
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from build_radar_data import build_data, display_score, raw_score, validate_raw
import validate


def fixture(mid="test", score=85, active=True):
    dimensions = ("reasoning", "coding", "agentic", "long_context", "data_analysis", "creative_writing")
    return {"id": mid, "name": mid, "provider": "test", "country": "US",
            "last_updated": "2026-10-21", "is_active": active,
            "evaluated_version": "keep-me",
            "dimensions": {key: {"score": score, "tier": "A", "source_tier": "T1_Benchmark",
                                 "confidence": "low", "evidence": "test evidence",
                                 "sources": ["https://example.com/benchmark"]} for key in dimensions}}


class PipelineTests(unittest.TestCase):
    def test_weighted_all_sources(self):
        self.assertEqual(raw_score(dict(score=99, vendor_score=80, third_party_score=90, community_score=70)), 81.5)

    def test_missing_sources_renormalize(self):
        self.assertEqual(raw_score(dict(score=99, vendor_score=80, third_party_score=90)), 86.4)
        self.assertEqual(raw_score(dict(score=99, community_score=70)), 70)

    def test_zero_is_present_and_all_null_falls_back(self):
        self.assertEqual(raw_score(dict(score=85, vendor_score=0)), 0)
        self.assertEqual(raw_score(dict(score=85, vendor_score=None)), 85)

    def test_fixed_anchors_clamping_and_curvature(self):
        self.assertEqual([display_score(s) for s in (0, 60, 98, 100)], [22.0, 22.0, 96.0, 96.0])
        self.assertEqual(display_score(79), 51.0)
        self.assertLess(display_score(79), 59)  # Below linear midpoint.

    def test_filtering_order_and_rank(self):
        output = build_data([fixture("z", 95), fixture("off", 100, False), fixture("b", 80), fixture("a", 95)])
        self.assertEqual([(m["id"], m["rank"]) for m in output["models"]], [("b", 3), ("z", 2), ("a", 1)])

    def test_presentation_counts_through_ties_in_both_directions(self):
        models = [fixture("z", 95), fixture("b", 80), fixture("a", 95), fixture("c", 80)]
        for ascending, expected in [(True, [4, 3, 2, 1]), (False, [1, 2, 3, 4])]:
            with self.subTest(ascending=ascending), patch("build_radar_data.SORT_ASCENDING", ascending):
                result = build_data(models)["models"]
                self.assertEqual([m["rank"] for m in result], expected)
                self.assertEqual({m["id"]: m["rank"] for m in result}, {"a": 1, "z": 2, "b": 3, "c": 4})

    def test_build_does_not_mutate_raw_or_drop_metadata(self):
        models = [fixture()]
        before = copy.deepcopy(models)
        result = build_data(models)["models"][0]
        self.assertEqual(models, before)
        self.assertEqual(result["evaluated_version"], "keep-me")
        self.assertTrue(result["dimensions"]["coding"]["is_low_confidence"])
        self.assertEqual(result["dimensions"]["coding"]["score_method"], "legacy_score")

    def test_weighted_tier_follows_new_score(self):
        m = fixture(score=85)
        m["dimensions"]["coding"]["third_party_score"] = 95
        result = build_data([m])["models"][0]
        self.assertEqual(result["dimensions"]["coding"]["tier"], "S")
        self.assertEqual(result["dimensions"]["coding"]["score"], 95)
        self.assertEqual(result["dimensions"]["coding"]["raw_score"], 95)
        self.assertEqual(m["dimensions"]["coding"]["score"], 85)
        self.assertEqual(m["dimensions"]["coding"]["tier"], "A")

    def test_overall_thresholds(self):
        for score, tier in [(79.9, "B"), (80, "A"), (85, "S"), (90, "S+")]:
            self.assertEqual(build_data([fixture(score=score)])["models"][0]["overall_tier"], tier)

    def test_invalid_scores_rejected(self):
        for field in ("score", "vendor_score", "third_party_score", "community_score"):
            for score in (True, "90", -1, 101, float("nan"), float("inf")):
                m = fixture()
                m["dimensions"]["coding"][field] = score
                with self.subTest(field=field, score=score), self.assertRaises(ValueError):
                    build_data([m])

    def test_missing_dimensions_duplicate_ids_and_boolean_switch(self):
        m = fixture()
        del m["dimensions"]
        self.assertTrue(validate_raw([m]))
        self.assertTrue(validate_raw([fixture(), fixture()]))
        self.assertTrue(validate_raw([fixture(active="false")]))

    def test_empty_active_set_supported(self):
        self.assertEqual(build_data([fixture(active=False)])["models"], [])

    def test_validator_rejects_missing_or_stale_processed(self):
        with tempfile.TemporaryDirectory() as tmp:
            raw, out = Path(tmp) / "raw.json", Path(tmp) / "out.json"
            models = [fixture()]
            raw.write_text(json.dumps(models))
            with patch.object(validate, "RAW_FILE", raw), patch.object(validate, "OUTPUT_FILE", out), \
                    patch("builtins.print"):
                self.assertEqual(validate.main(), 1)
                derived = build_data(models)
                out.write_text(json.dumps(derived))
                self.assertEqual(validate.main(), 0)
                derived["models"][0]["dimensions"]["coding"]["raw_score"] = 99
                out.write_text(json.dumps(derived))
                self.assertEqual(validate.main(), 1)

    def test_confidence_evidence_and_source_validation(self):
        for field, value in [("confidence", "certain"), ("evidence", ""), ("sources", []), ("raw_metrics", [])]:
            m = fixture()
            m["dimensions"]["coding"][field] = value
            self.assertTrue(validate_raw([m]))

    def test_cli_preserves_output_on_failure_and_raw_on_success(self):
        with tempfile.TemporaryDirectory() as tmp:
            raw, out = Path(tmp) / "raw.json", Path(tmp) / "out.json"
            raw.write_text(json.dumps([fixture()]))
            before = raw.read_bytes()
            cmd = [sys.executable, str(ROOT / "scripts/build_radar_data.py"), "--input", str(raw), "--output", str(out)]
            result = subprocess.run(cmd, capture_output=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(raw.read_bytes(), before)
            output_before = out.read_bytes()
            result = subprocess.run(cmd, capture_output=True)
            self.assertEqual(result.returncode, 0)
            self.assertEqual(out.read_bytes(), output_before)
            raw.write_text('[invalid')
            self.assertNotEqual(subprocess.run(cmd, capture_output=True).returncode, 0)
            self.assertEqual(out.read_bytes(), output_before)
            raw.write_bytes(before)
            same = cmd[:-1] + [str(raw)]
            self.assertNotEqual(subprocess.run(same, capture_output=True).returncode, 0)
            self.assertEqual(raw.read_bytes(), before)


if __name__ == "__main__":
    unittest.main()
