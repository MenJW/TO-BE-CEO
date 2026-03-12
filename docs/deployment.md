# Deployment

This repository now includes a minimal online demo deployment path for Render.

## What Is Included

- A production WSGI entrypoint at src/intelligent_brain_company/wsgi.py
- A Render blueprint file at render.yaml
- Gunicorn as the non-Windows production server dependency

## Render Quick Path

1. Push the repository to GitHub.
2. In Render, choose New + Blueprint.
3. Select this repository.
4. Render will detect render.yaml and create the web service.
5. Set environment variables if you want live LLM-backed stages.

## Required Runtime Variables

- IBC_HOST: set to 0.0.0.0 for cloud deployment
- IBC_PORT: provided by Render through PORT, kept in sync in render.yaml
- IBC_DATA_DIR: writable persistent path, set to /var/data/ibc in render.yaml

## Optional LLM Variables

- IBC_LLM_API_KEY
- IBC_LLM_BASE_URL
- IBC_LLM_MODEL
- IBC_LLM_TIMEOUT_SECONDS

If these are not set, the app still works as a deterministic demo.

## Demo Deployment Notes

- The current Render config is intended for a public product demo, not a hardened production environment.
- SQLite is acceptable for a single-instance demo deployment, but do not treat it as a multi-instance production database.
- The current app has no authentication. If you expose it publicly, treat it as a showcase environment.

## Local Verification Before Deploy

```bash
python -m pip install -e .[dev]
ibc-api
```

Open http://127.0.0.1:8000 and verify:

1. A demo project can be created.
2. A plan can be generated.
3. A chat turn can be promoted into an intervention.
4. A plan diff appears after regeneration.

## Recommended Next Production Upgrades

1. Add authentication.
2. Replace SQLite with a managed database for multi-user deployment.
3. Add request rate limiting.
4. Add a demo data reset task.
5. Add observability and error reporting.