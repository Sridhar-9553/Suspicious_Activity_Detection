from pathlib import Path
import os
import shutil, uuid
import cv2
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware


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
    return {"status": "ok", "model_ready": False, "message": "Notebook model integration is pending."}


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
            path.unlink(missing_ok=True)
            raise HTTPException(400, "Could not read this video. Please try another file.")
        fps = cap.get(cv2.CAP_PROP_FPS) or 0
        frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) or 0)
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) or 0)
        cap.release()
