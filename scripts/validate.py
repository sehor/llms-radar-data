"""Validate raw evidence and detect missing/stale derived data."""
import json
import sys
from build_radar_data import RAW_FILE, OUTPUT_FILE, DIMENSIONS, build_data, validate_raw


def main():
    try:
        models = json.loads(RAW_FILE.read_text(encoding='utf-8-sig'))
        errors = validate_raw(models)
        if errors:
            raise ValueError('\n'.join(errors))
        processed = json.loads(OUTPUT_FILE.read_text(encoding='utf-8-sig'))
        if processed != build_data(models):
            raise ValueError('Derived data is stale or invalid; run python scripts/build_radar_data.py')
    except (OSError, ValueError, TypeError) as exc:
        print(f'Validation failed: {exc}', file=sys.stderr)
        return 1
    print(f"Models: {len(models)}; active: {sum(m['is_active'] for m in models)}")
    for dimension in DIMENSIONS:
        print(f'{dimension}: {len(models)}/{len(models)}')
    low = sum(d['confidence'] == 'low' for m in models for d in m['dimensions'].values())
    print(f'Low confidence dimensions (including inactive models): {low}')
    print('Validation passed: raw fields, evidence and derived output are consistent.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
