from pathlib import Path
import os
import shutil, uuid
import cv2
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette.concurrency import run_in_threadpool

from model_inference import analyze_video as run_model_analysis, is_model_file_available

ROOT = Path(__file__).parent
UPLOADS = ROOT / "uploads"
UPLOADS.mkdir(exist_ok=True)
ALLOWED = {".mp4", ".avi", ".mov", ".mkv"}
app = FastAPI(title="Sentinel AI Video Analysis API", version="0.1.0")
allowed_origins = []
for origin in os.getenv("ALLOWED_ORIGINS", "http://localhost:5173").split(","):
    origin = origin.strip().rstrip("/")
    if origin:
        allowed_origins.append(origin if "://" in origin else f"https://{origin}")
app.add_middleware(CORSMiddleware, allow_origins=allowed_origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

@app.get("/api/health")
def health():
    available = is_model_file_available()
    return {
        "status": "ok",
        "model_ready": available,
        "message": "Model weights are available." if available else "Model weights were not found.",
    }

@app.post("/api/analyze")
async def analyze_video(video: UploadFile = File(...)):
    ext = Path(video.filename or "video.mp4").suffix.lower()
    if ext not in ALLOWED:
        raise HTTPException(400, "Unsupported video format. Upload MP4, AVI, MOV, or MKV.")
    file_id = uuid.uuid4().hex
    path = UPLOADS / f"{file_id}{ext}"
    try:
        with path.open("wb") as out:
            shutil.copyfileobj(video.file, out)
        cap = cv2.VideoCapture(str(path))
        if not cap.isOpened():
            raise HTTPException(400, "Could not read this video. Please try another file.")
        fps = cap.get(cv2.CAP_PROP_FPS) or 0
        frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) or 0)
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) or 0)
        cap.release()
        if not is_model_file_available():
            raise HTTPException(
                503,
                "The trained model weights are missing. Add best_model.keras to "
                "runs/ or Backend/models/, or configure MODEL_PATH on the backend.",
            )
        try:
            predictions = await run_in_threadpool(run_model_analysis, path, fps, frames)
        except FileNotFoundError as exc:
            raise HTTPException(503, str(exc)) from exc
        except ValueError as exc:
            raise HTTPException(400, str(exc)) from exc
        return {
            "video_id": file_id, "filename": video.filename,
            "metadata": {"duration_seconds": round(frames / fps, 2) if fps > 0 else None, "fps": round(fps, 2), "frames": frames, "width": width, "height": height},
            "model_ready": True,
            "status": "analyzed",
            "message": "Video scored in two-second windows. The overall result is suspicious when any window exceeds the model threshold.",
            **predictions,
        }
    finally:
        await video.close()

@app.get("/api/history")
def history():
    return {"items": []}
