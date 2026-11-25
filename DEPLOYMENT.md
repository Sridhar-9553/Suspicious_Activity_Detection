# Deploy Sentinel AI with Streamlit Community Cloud

The Streamlit app runs the interface and video model in the same service; it does not need a separate API service.

1. Confirm the repository contains `Backend/streamlit_app.py`, root `requirements.txt`, and `Backend/models/final_model.keras`.
2. Open [Streamlit Community Cloud](https://share.streamlit.io/) and create an app from the GitHub repository.
3. Select branch `main`, set the app file path to `Backend/streamlit_app.py`, and choose Python 3.11 in advanced settings.
4. Deploy and share the resulting app URL.

The root `requirements.txt` installs the model dependencies from `Backend/requirements.txt` plus Streamlit. The first video analysis downloads ImageNet ResNet50 weights unless cached, so the first run can take longer. Streamlit hosting resources may be insufficient for TensorFlow or long videos; confirm the current plan's memory limits before sharing the app widely.

Uploads are stored temporarily during analysis and deleted afterward. Do not use this prototype to store sensitive footage. The model scores two-second intervals using a 0.705 threshold. Results can be wrong and require human review; they are not proof of criminal activity.

## Existing Render deployment

The repository also includes `render.yaml` for the separate React/FastAPI deployment. Its free backend restarted when an analysis loaded the ResNet50 model, so it is not reliable for video analysis on that plan. No paid Render service has been selected.
