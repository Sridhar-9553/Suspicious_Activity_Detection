import tempfile
from pathlib import Path

import cv2
import streamlit as st


SUPPORTED_EXTENSIONS = {".mp4", ".avi", ".mov", ".mkv"}
MAX_UPLOAD_SIZE_MB = 200


def analyze_uploaded_video(uploaded_file):
    extension = Path(uploaded_file.name).suffix.lower()
    if extension not in SUPPORTED_EXTENSIONS:
        raise ValueError("Upload an MP4, AVI, MOV, or MKV video.")

    with tempfile.TemporaryDirectory(prefix="sentinel-ai-") as temp_dir:
        video_path = Path(temp_dir) / f"upload{extension}"
        with video_path.open("wb") as output_file:
            output_file.write(uploaded_file.getbuffer())

        capture = cv2.VideoCapture(str(video_path))
        try:
            if not capture.isOpened():
                raise ValueError("Could not read this video. Please try another file.")
            fps = capture.get(cv2.CAP_PROP_FPS) or 0
            frame_count = int(capture.get(cv2.CAP_PROP_FRAME_COUNT) or 0)
        finally:
            capture.release()

        if fps <= 0 or frame_count <= 0:
            raise ValueError("This video has invalid frame-rate or frame-count metadata.")

        from model_inference import analyze_video

        return analyze_video(video_path, fps, frame_count)


def render_results(result):
    summary = result["summary"]
    if summary["label"] == "SUSPICIOUS":
        st.warning(
            "The model flagged one or more intervals. Review the footage; "
            "this result is not proof of criminal activity."
        )
    else:
        st.info("The model did not flag any intervals. This does not guarantee the video is safe.")

    metric_columns = st.columns(3)
    metric_columns[0].metric("Overall result", summary["label"])
    metric_columns[1].metric("Confidence", f"{summary['confidence']:.1%}")
    metric_columns[2].metric("Flagged intervals", summary["clips_suspicious"])

    clip_rows = [
        {
            "Interval": f"{clip['start_seconds']:.2f} - {clip['end_seconds']:.2f} s",
            "Prediction": clip["label"],
            "Confidence": f"{clip['confidence']:.1%}",
            "Suspicious probability": f"{clip['suspicious_probability']:.1%}",
        }
        for clip in result["clips"]
    ]
    st.subheader("Two-second interval results")
    st.dataframe(clip_rows, hide_index=True, use_container_width=True)


st.set_page_config(page_title="Sentinel AI", page_icon="🎥", layout="centered")
st.title("Sentinel AI")
st.subheader("Suspicious Activity Detection")
st.write("Upload surveillance footage for AI-assisted review.")
st.caption(
    "The model scores two-second intervals. Results can be wrong and require human review; "
    "they are not proof of criminal activity."
)

uploaded_file = st.file_uploader(
    "Choose a video",
    type=sorted(extension.removeprefix(".") for extension in SUPPORTED_EXTENSIONS),
    max_upload_size=MAX_UPLOAD_SIZE_MB,
)

upload_signature = (
    (uploaded_file.name, uploaded_file.size) if uploaded_file is not None else None
)
if st.session_state.get("upload_signature") != upload_signature:
    st.session_state["upload_signature"] = upload_signature
    st.session_state.pop("analysis_result", None)

if st.button("Analyze video", type="primary", disabled=uploaded_file is None):
    try:
        with st.spinner("Loading the AI model and analyzing the video..."):
            st.session_state["analysis_result"] = analyze_uploaded_video(uploaded_file)
    except (FileNotFoundError, ValueError) as error:
        st.session_state.pop("analysis_result", None)
        st.error(str(error))

if result := st.session_state.get("analysis_result"):
    render_results(result)
