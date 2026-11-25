# Deploy Sentinel AI on Render

1. In Render, choose **New → Blueprint** and connect this repository. Render reads `render.yaml` and creates the API and frontend services.
2. Copy the public hostname assigned to the `sentinel-ai-api` service. In the `sentinel-ai-frontend` service settings, set `VITE_API_HOST` to that hostname (without `https://`), then trigger a new deploy.
3. Copy the frontend service URL. Set the API service environment variable `ALLOWED_ORIGINS` to the complete frontend URL, including `https://`, and redeploy/restart the API.
4. Open and share the frontend service URL.

The API currently validates uploaded videos and returns metadata only; the notebook model is not connected, so it does not classify activity. Uploaded videos are stored on the API instance disk and may be removed by a restart or redeploy. Do not upload sensitive footage. Free services can sleep when idle and take longer to respond to the first request.
