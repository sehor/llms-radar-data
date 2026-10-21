"""Build derived radar data without modifying the evidence database (stdlib only)."""
import argparse
import copy
import json
import math
import os
import sys
import tempfile
from pathlib import Path

WEIGHTS = {"vendor": 0.25, "third_party": 0.45, "community": 0.30}
FLOOR = 60.0
CEILING = 98.0
MIN_RADIUS = 22.0
MAX_RADIUS = 96.0
GAMMA = 1.35
SORT_ASCENDING = True

ROOT = Path(__file__).resolve().parents[1]
RAW_FILE = ROOT / "data/raw/models.json"
OUTPUT_FILE = ROOT / "data/processed/radar_ready.json"
DIMENSIONS = ("reasoning", "coding", "agentic", "long_context", "data_analysis", "creative_writing")
SCORE_FIELDS = tuple(f"{source}_score" for source in WEIGHTS)


def valid_score(value):
    return (isinstance(value, (int, float)) and not isinstance(value, bool)
            and math.isfinite(value) and 0 <= value <= 100)


def validate_raw(models):
    errors = []
    if not isinstance(models, list):
        return ["top-level JSON value must be an array"]
    seen = set()
    for index, model in enumerate(models):
        path = f"models[{index}]"
        if not isinstance(model, dict):
            errors.append(f"{path} must be an object")
            continue
        for field in ("id", "name", "provider", "country", "last_updated"):
            if not isinstance(model.get(field), str) or not model[field].strip():
                errors.append(f"{path}.{field} must be a nonempty string")
        mid = model.get("id")
        if isinstance(mid, str):
            if mid in seen:
                errors.append(f"{path}.id is duplicated: {mid}")
            seen.add(mid)
        if type(model.get("is_active")) is not bool:
            errors.append(f"{path}.is_active must be boolean")
        dims = model.get("dimensions")
        if not isinstance(dims, dict):
            errors.append(f"{path}.dimensions must contain all six dimensions")
            continue
        for key in DIMENSIONS:
            dim = dims.get(key)
            dp = f"{path}.dimensions.{key}"
            if not isinstance(dim, dict):
                errors.append(f"{dp} must be an object")
                continue
            if not valid_score(dim.get("score")):
                errors.append(f"{dp}.score must be finite and between 0 and 100")
            for field in SCORE_FIELDS:
                if dim.get(field) is not None and not valid_score(dim[field]):
                    errors.append(f"{dp}.{field} must be null or finite between 0 and 100")
            if "raw_metrics" in dim and not isinstance(dim["raw_metrics"], dict):
                errors.append(f"{dp}.raw_metrics must be an object")
            if dim.get("tier") not in {"S", "A", "B", "C"}:
                errors.append(f"{dp}.tier is invalid")
            if dim.get("source_tier") not in {"T1_Benchmark", "T2_Community", "T3_Estimated"}:
                errors.append(f"{dp}.source_tier is invalid")
            if dim.get("confidence") not in {"high", "medium", "low"}:
                errors.append(f"{dp}.confidence is invalid")
            if not isinstance(dim.get("evidence"), str) or not dim["evidence"].strip():
                errors.append(f"{dp}.evidence must be nonempty")
            sources = dim.get("sources")
            if (not isinstance(sources, list) or not sources
                    or any(not isinstance(s, str) or not s.startswith(("https://", "http://")) for s in sources)):
                errors.append(f"{dp}.sources must be a nonempty list of URLs")
    return errors


def raw_score(dimension):
    available = [(dimension[f"{source}_score"], weight)
                 for source, weight in WEIGHTS.items()
                 if dimension.get(f"{source}_score") is not None]
    if not available:
        return round(dimension["score"], 1)
    return round(sum(score * weight for score, weight in available)
                 / sum(weight for _, weight in available), 1)


def display_score(score):
    normalized = (max(FLOOR, min(CEILING, score)) - FLOOR) / (CEILING - FLOOR)
    return round(MIN_RADIUS + normalized ** GAMMA * (MAX_RADIUS - MIN_RADIUS), 1)


def dimension_tier(score):
    return "S" if score >= 90 else "A" if score >= 80 else "B" if score >= 70 else "C"


def overall_tier(score):
    return "S+" if score >= 90 else "S" if score >= 85 else "A" if score >= 80 else "B"


def build_data(models):
    if (not all(math.isfinite(v) and v > 0 for v in WEIGHTS.values())
            or not FLOOR < CEILING or not MIN_RADIUS < MAX_RADIUS or not GAMMA > 0):
        raise ValueError("Invalid weighting or display constants")
    errors = validate_raw(models)
    if errors:
        raise ValueError("\n".join(errors))
    output = []
    for model in models:
        if model["is_active"] is not True:
            continue
        item = copy.deepcopy(model)
        for key in DIMENSIONS:
            dim = item["dimensions"][key]
            score = raw_score(dim)
            dim.update(score=score, raw_score=score, display_score=display_score(score),
                       tier=dimension_tier(score), is_low_confidence=dim["confidence"] == "low",
                       score_method="weighted" if any(dim.get(f) is not None for f in SCORE_FIELDS) else "legacy_score")
        item["overall_score"] = round(sum(item["dimensions"][k]["raw_score"] for k in DIMENSIONS) / len(DIMENSIONS), 1)
        item["overall_tier"] = overall_tier(item["overall_score"])
        output.append(item)
    # Strength rank is independent of presentation order. ID breaks ties reproducibly.
    ranked = sorted(output, key=lambda m: (-m["overall_score"], m["id"]))
    for rank, item in enumerate(ranked, 1):
        item["rank"] = rank
    output.sort(key=lambda m: -m["rank"] if SORT_ASCENDING else m["rank"])
    return {"schema_version": "1.0", "dimension_order": list(DIMENSIONS),
            "scoring": {"weights": WEIGHTS.copy(), "floor": FLOOR, "ceiling": CEILING,
                        "min_radius": MIN_RADIUS, "max_radius": MAX_RADIUS, "gamma": GAMMA,
                        "sort_ascending": SORT_ASCENDING, "rank_order": "descending_score_then_id"},
            "models": output}


def atomic_write(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=path.parent, delete=False) as f:
            temp = f.name
            f.write(content)
        os.replace(temp, path)
    finally:
        if temp and os.path.exists(temp):
            os.unlink(temp)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=RAW_FILE)
    parser.add_argument("--output", type=Path, default=OUTPUT_FILE)
    args = parser.parse_args()
    try:
        if args.input.resolve() == args.output.resolve():
            raise ValueError("Output must not overwrite the raw input")
        data = build_data(json.loads(args.input.read_text(encoding="utf-8-sig")))
        atomic_write(args.output, json.dumps(data, ensure_ascii=False, indent=2, allow_nan=False) + "\n")
    except (OSError, ValueError, TypeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(f"Built {len(data['models'])} active models -> {args.output}")
    for model in sorted(data["models"], key=lambda m: m["rank"]):
        print(f"{model['rank']:2}. {model['name']}: {model['overall_score']:.1f} ({model['overall_tier']})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
