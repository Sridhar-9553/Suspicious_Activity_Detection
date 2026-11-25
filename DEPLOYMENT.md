# Deploy Sentinel AI on Render

The Render Blueprint creates a FastAPI backend and a static React frontend from the root `render.yaml`. The trained `best_model.keras` file is stored at `Backend/models/best_model.keras`; this file is included in the public GitHub repository.

1. In Render, choose **New → Blueprint** and connect this repository.
2. Set `VITE_API_HOST` on the frontend service to the backend's public hostname without `https://`, then redeploy the frontend.
3. Set `ALLOWED_ORIGINS` on the backend to the frontend's complete public URL, including `https://`, then redeploy/restart the backend.
4. Open and share the frontend service URL.

The backend also needs ImageNet ResNet50 weights. TensorFlow downloads these on its first model initialization unless they are already cached. TensorFlow plus ResNet50 needs more memory than a minimal API; a free backend may restart or fail under load. A larger instance may be required. Do not select or authorize a paid plan without reviewing its cost.

Uploaded footage is stored on the backend instance's local disk and may be removed by a restart or redeploy. Do not use this prototype to store sensitive footage. The model flags two-second intervals using a 0.705 threshold. Results can be wrong and require human review; they are not proof of criminal activity.
