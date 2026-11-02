# SentinelAI Chromium browser QA

Playwright + Chromium provides isolated browser smoke tests for the Next.js dashboard. It is used only in development and CI, not in the FastAPI event-ingestion runtime.

The suite checks initial page rendering, uncaught browser exceptions, and horizontal overflow at mobile (390px), tablet (768px), and desktop (1365px) viewports. It does not generate events, submit telemetry, or perform response actions.

## Local run

Start the frontend from `frontend/` using the existing package scripts. In another terminal from the repository root:

```bash
python -m pip install -r tests/browser/requirements.txt
python -m playwright install chromium
python -m pytest -q tests/browser
```

Set `SENTINELAI_BASE_URL` when using a different local URL. Use synthetic data only. These checks are not a full SOC workflow or security test.
