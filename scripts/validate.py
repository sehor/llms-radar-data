import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT / "data" / "raw" / "models.json"
DIMENSIONS = ("agentic", "coding", "reasoning", "long_context", "creative_writing", "data_analysis")
SOURCES = {"T1_Benchmark", "T2_Community", "T3_Estimated"}
TIERS = {"S", "A", "B", "C", "N/A"}


def main() -> int:
    try:
        models = json.loads(DATA_FILE.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: cannot read valid JSON at {DATA_FILE}: {exc}", file=sys.stderr)
        return 1
    if not isinstance(models, list):
        print("ERROR: top-level JSON value must be an array", file=sys.stderr)
        return 1
    errors = []
    for index, model in enumerate(models):
        label = f"models[{index}]"
        if not isinstance(model, dict):
            errors.append(f"{label} must be an object")
            continue
        for field in ("id", "name", "provider", "country", "last_updated"):
            if model.get(field) in (None, ""):
                errors.append(f"{label}.{field} is required")
        dims = model.get("dimensions")
        if dims is None:
            continue
        if not isinstance(dims, dict):
            errors.append(f"{label}.dimensions must be an object when present")
            continue
        for dimension in DIMENSIONS:
            value = dims.get(dimension)
            path = f"{label}.dimensions.{dimension}"
            if not isinstance(value, dict):
                errors.append(f"{path} must be an object")
                continue
            for field in ("score", "tier", "source_tier", "evidence"):
                if field not in value:
                    errors.append(f"{path}.{field} is required")
            score = value.get("score")
            if score is None:
                errors.append(f"{path}.score is null (dimension is unfilled)")
            elif isinstance(score, bool) or not isinstance(score, (int, float)) or not 0 <= score <= 100:
                errors.append(f"{path}.score must be a number from 0 to 100 or null")
            if value.get("tier") not in TIERS:
                errors.append(f"{path}.tier is invalid")
            source = value.get("source_tier")
            if source is not None and source not in SOURCES:
                errors.append(f"{path}.source_tier is invalid")
            if not isinstance(value.get("evidence"), str):
                errors.append(f"{path}.evidence must be a string")
    print(f"Models: {len(models)}")
    for dimension in DIMENSIONS:
        complete = sum(
            isinstance(model, dict)
            and isinstance(model.get("dimensions"), dict)
            and isinstance(model["dimensions"].get(dimension), dict)
            and model["dimensions"][dimension].get("score") is not None
            for model in models
        )
        print(f"{dimension}: {complete}/{len(models)}")
    if errors:
        print("Validation failed:", file=sys.stderr)
        print("\n".join(f"- {error}" for error in errors), file=sys.stderr)
        return 1
    print("Validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
