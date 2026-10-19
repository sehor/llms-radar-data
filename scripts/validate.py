import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "raw" / "models.json"
DIMENSIONS = ("agentic", "coding", "reasoning", "long_context", "creative_writing", "data_analysis")
TIERS = {"S", "A", "B", "C", "N/A"}
SOURCES = {"T1_Benchmark", "T2_Community", "T3_Estimated"}


def main():
    try:
        models = json.loads(DATA.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"Invalid JSON or unreadable file: {exc}", file=sys.stderr)
        return 1
    if not isinstance(models, list):
        print("Top-level value must be an array", file=sys.stderr)
        return 1
    errors = []
    for i, model in enumerate(models):
        label = f"models[{i}]"
        if not isinstance(model, dict):
            errors.append(f"{label} must be an object")
            continue
        for key in ("id", "name", "provider", "last_updated", "dimensions"):
            if model.get(key) in (None, ""):
                errors.append(f"{label}.{key} is required")
        dims = model.get("dimensions")
        if not isinstance(dims, dict):
            errors.append(f"{label}.dimensions must be an object")
            continue
        for dim in DIMENSIONS:
            item = dims.get(dim)
            path = f"{label}.dimensions.{dim}"
            if not isinstance(item, dict):
                errors.append(f"{path} must be an object")
                continue
            for key in ("score", "tier", "source_tier", "evidence"):
                if key not in item:
                    errors.append(f"{path}.{key} is required")
            score = item.get("score")
            if score is None:
                errors.append(f"{path}.score is null (unfilled)")
            elif isinstance(score, bool) or not isinstance(score, (int, float)) or not 0 <= score <= 100:
                errors.append(f"{path}.score must be 0-100 or null")
            if item.get("tier") not in TIERS:
                errors.append(f"{path}.tier is invalid")
            if item.get("source_tier") is not None and item.get("source_tier") not in SOURCES:
                errors.append(f"{path}.source_tier is invalid")
            if not isinstance(item.get("evidence"), str):
                errors.append(f"{path}.evidence must be a string")
    print(f"Models: {len(models)}")
    for dim in DIMENSIONS:
        full = sum(isinstance(m, dict) and isinstance(m.get("dimensions"), dict) and isinstance(m["dimensions"].get(dim), dict) and m["dimensions"][dim].get("score") is not None for m in models)
        print(f"{dim}: {full}/{len(models)}")
    if errors:
        print("Validation failed:", file=sys.stderr)
        print("\\n".join(f"- {e}" for e in errors), file=sys.stderr)
        return 1
    print("Validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
