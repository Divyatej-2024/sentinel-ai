# Public demo deployment on Render

The repository includes a Render Blueprint that provisions the Next.js frontend, FastAPI service, and PostgreSQL database in Frankfurt. Both web services receive public `onrender.com` URLs. The backend generates an API key and requires `X-API-Key` on every event endpoint when deployed.

## Deploy

1. Push this repository, including `render.yaml`, to GitHub.
2. Sign in to Render and choose **New > Blueprint**.
3. Connect `Divyatej-2024/sentinel-ai` and deploy the Blueprint from the branch containing this file.
4. Wait for the API health check and frontend build to pass. Open the `sentinelai-web` service URL.
5. Copy the generated `API_KEY` from the API service environment page and store it securely. Send it as `X-API-Key` when calling `/api/v1/events`.

If the API service name is unavailable in your Render workspace, rename it and update the frontend's `NEXT_PUBLIC_API_URL` to the resulting API URL, then redeploy the frontend. Render injects Docker service environment values during image builds, which lets Next.js bake the API URL into the frontend.

## Free-tier limits

The Blueprint deliberately uses free plans so initial deployment does not create a paid resource. Render free web services sleep after 15 minutes without traffic, and free PostgreSQL databases expire after 30 days. The database has a 14-day recovery window after expiry, after which its data is deleted. This is suitable for a temporary public demo with synthetic data, not a persistent service. For an always-on site and durable event storage, change the service/database plans in `render.yaml` to paid plans before deploying; Render charges for those resources.

Do not send real security telemetry to this public demo. API-key authentication is shared-secret protection, not analyst accounts or per-user authorization.
