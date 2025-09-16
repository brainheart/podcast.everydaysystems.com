# Scripts Overview

This directory contains maintenance and build scripts for the podcast portion of the site.

## Permanent Scripts

- `build_index.py` — Generates `index.html` from `metadata/episodes.json`. Run:
  ```bash
  python scripts/build_index.py
  # or specify an alternate output file
  python scripts/build_index.py --out index.preview.html
  ```
- `check_year_counts.py`, `cleanup_year_includes.py`, `fix_year_include.py` — Historical utilities used to normalize footer year script tags (kept for provenance/re-run if needed).
- `remove_ga.py`, `replace_podcast_dotdot.py`, `newline_spans_episode96.py` — One-time content fixers that were useful during cleanup. They remain tracked so their intent is documented.

## One-off / Scratch Scripts

Ad-hoc or experimental throwaway scripts should live in:

```
scripts/oneoff/
```

That path is git-ignored (see root `.gitignore`), so you can drop quick experiments there without polluting version control.

If a one-off script becomes generally useful, move it up one level and document it here under **Permanent Scripts**.

## Conventions

- Keep scripts idempotent when possible (safe to re-run).
- Avoid hard-coding absolute paths; derive from project root like `build_index.py`.
- Prefer read-only dry runs (e.g., add a `--dry-run` flag) for destructive operations — future enhancement.

## Future Enhancements (Optional)

- Add a `make build-index` target (or simple shell wrapper) for convenience.
- Add a validation script to check that every episode directory has an entry in `episodes.json` and vice-versa.
- Introduce a lightweight test that asserts the number of `<table>` blocks in `index.html` equals the number of episode objects.

