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

**Current status:** upload validation and video metadata work. The Kaggle notebook model is not connected yet; endpoint deliberately returns `awaiting_model` rather than fabricating predictions. Review notebook preprocessing, architecture, class labels, weights and inference code before implementing model loading.
