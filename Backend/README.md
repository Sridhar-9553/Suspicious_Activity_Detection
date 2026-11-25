# Sentinel AI backend

## Setup
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

API: `GET /api/health`, `POST /api/analyze` (multipart field `video`), `GET /api/history`.

The backend loads `runs/best_model.keras` by default, then checks `Backend/models/best_model.keras` (the committed deployment copy). Override the location with `MODEL_PATH`; relative paths are resolved from this backend folder. Model inference matches the notebook: ImageNet ResNet50 features, 16 sampled frames per two-second clip, and a 0.705 threshold. Each upload returns per-clip scores and flagged intervals. The model's ImageNet weights may need to download the first time ResNet50 initializes.

The health endpoint reports whether a saved model file is available. The AI output is a screening aid and must be reviewed by a person.
