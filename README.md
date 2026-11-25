# Sentinel AI — suspicious activity video website

[Try Sentinel AI](https://suspiciousactivitydetection-p3kzmupgydqmprz42hnzlg.streamlit.app/)  - Test your own video

**Resources:** [Dataset](https://www.kaggle.com/datasets/daudshah/video-dataset) \n
· [Report (PDF)](https://docs.google.com/gview?embedded=1&url=https%3A%2F%2Fraw.githubusercontent.com%2FSridhar-9553%2FSuspicious_Activity_Detection%2Fmain%2FVA_report.pdf) \n
· [Suspicious Activity Detector (PowerPoint)](https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Fraw.githubusercontent.com%2FSridhar-9553%2FSuspicious_Activity_Detection%2Fmain%2Fcriminal_activity_detector_report.pptx)


Sentinel AI is a React frontend with a FastAPI backend. It uses a ResNet50 feature extractor and a trained temporal classifier to score uploaded surveillance videos in two-second windows.

The backend expects the `final_model.keras` weights from the notebook. Locally it finds `runs/final_model.keras` automatically; otherwise set `MODEL_PATH` to the model file's absolute path. It samples 16 frames per two-second window, preprocesses them as in the notebook, and uses the validation-tuned threshold of `0.705`. The overall video is marked suspicious if any window crosses the threshold.

> **Important:** This is an AI-assisted screening tool, not proof of criminal activity. Results can be wrong and require human review. Uploaded videos are stored on the backend instance's local disk.
>
> The saved `final_model.keras` file is published at `Backend/models/final_model.keras` in the public GitHub repository. The pretrained ImageNet ResNet50 weights are separate and are downloaded on first model initialization.

## Deploy a public Streamlit app

The Streamlit version combines the interface and model inference in one app. The React/FastAPI version remains available as a separate option.

1. Push the repository to GitHub with `Backend/streamlit_app.py`, the root `requirements.txt`, and `Backend/models/final_model.keras`.
2. In [Streamlit Community Cloud](https://share.streamlit.io/), create an app from this repository's `main` branch and set the app file to `Backend/streamlit_app.py`.
3. Choose Python 3.11 in the app's advanced settings, then deploy.
4. Open and share the Streamlit app URL.

The first analysis downloads ImageNet ResNet50 weights if they are not cached. Streamlit Cloud's available memory can change; confirm that the selected hosting plan can load TensorFlow and process your video lengths. The app removes each temporary upload after analysis. Avoid uploading sensitive footage to a public demo.

## Deploy the React/FastAPI version with Render

1. Push this project to a GitHub repository. Make sure the repository includes `render.yaml`.
2. In [Render](https://render.com/), choose **New → Blueprint**, connect the GitHub repository, and deploy the two services described in `render.yaml`.
3. After the services are created, copy the public URL of the backend web service (for example, `https://sentinel-ai-api.onrender.com`).
4. Open the **frontend static site** in Render and add this environment variable:
   - `VITE_API_HOST` = the backend hostname, without `https://` (for example, `sentinel-ai-api.onrender.com`)
   Then trigger a new deploy so Vite builds the frontend with the backend address.
5. Copy the public URL of the frontend static site. In the **backend web service**, add:
   - `ALLOWED_ORIGINS` = the frontend URL, including `https://` (for example, `https://sentinel-ai-frontend.onrender.com`)
   Then restart/redeploy the backend.
6. Open the frontend URL. You can share that live URL; the GitHub repository link is for viewing or cloning the source code.

Render's free web services may sleep when idle, so the first request after a period of inactivity can take a while. TensorFlow and ResNet50 need substantially more memory than a minimal API; a free backend may restart or fail under load. The first model load also downloads ImageNet ResNet50 weights unless cached. Uploaded files are stored on the backend instance's local disk and may not persist across redeploys or restarts. Do not treat this prototype as a production service for sensitive footage.

## Run locally

Requirements: Python 3.11 or newer. Install the Streamlit and model dependencies from the repository root:

```powershell
python -m pip install -r requirements.txt
python -m streamlit run Backend/streamlit_app.py
```

Open `http://localhost:8501` to use the Streamlit app.

For the React/FastAPI version, Node.js and npm are also required. TensorFlow and its dependencies are installed from the backend requirements.

In PowerShell terminal 1:

```powershell
Set-Location 'backend'
..\.venv\Scripts\python.exe -m pip install -r requirements.txt
..\.venv\Scripts\python.exe -m uvicorn main:app --reload --port 8000
```

If the project-level `.venv` is not present, create it from the repository root with `python -m venv .venv` and install the backend requirements using `.venv\Scripts\python.exe -m pip install -r backend\requirements.txt`.

In PowerShell terminal 2:

```powershell
Set-Location 'frontend'
npm install
npm run dev
```

Open `http://localhost:5173`. Locally, the frontend uses `http://localhost:8000` by default.

## API

- `GET /api/health` — backend status
- `POST /api/analyze` — upload a video using multipart field `video`
- `GET /api/history` — placeholder history endpoint

Supported file extensions: MP4, AVI, MOV, and MKV.
