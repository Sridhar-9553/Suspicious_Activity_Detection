import os
from functools import lru_cache
from pathlib import Path
from threading import Lock

import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.applications.resnet50 import preprocess_input


ROOT = Path(__file__).parent
NUM_FRAMES = 16
IMAGE_SIZE = 224
CLIP_SECONDS = 2.0
THRESHOLD = 0.705


class TemporalAttention(tf.keras.layers.Layer):
    def __init__(self, **kwargs):
        kwargs.pop("score_config", None)
        super().__init__(**kwargs)
        self.score = tf.keras.layers.Dense(1, use_bias=True)

    def build(self, input_shape):
        self.score.build(input_shape)
        super().build(input_shape)

    def call(self, inputs):
        weights = tf.nn.softmax(self.score(inputs), axis=1)
        return tf.reduce_sum(weights * inputs, axis=1)

    def get_config(self):
        config = super().get_config()
        config["score_config"] = self.score.get_config()
        return config


class ActivityModel:
    def __init__(self, model_path: Path):
        if not model_path.is_file():
            raise FileNotFoundError(
                f"Trained model file was not found at {model_path}. "
                "Set MODEL_PATH or add final_model.keras to runs/ or Backend/models/."
            )
        self.model = tf.keras.models.load_model(
            model_path,
            custom_objects={
                "TemporalAttention": TemporalAttention,
                "CriminalDetector>TemporalAttention": TemporalAttention,
            },
            compile=False,
        )
        self.feature_extractor = ResNet50(
            include_top=False,
            weights="imagenet",
            pooling="avg",
            input_shape=(IMAGE_SIZE, IMAGE_SIZE, 3),
        )
        self.feature_extractor.trainable = False
        self._prediction_lock = Lock()

    def predict_clip(self, frames: np.ndarray) -> dict:
        processed_frames = np.stack(
            [
                cv2.resize(
                    cv2.cvtColor(frame, cv2.COLOR_BGR2RGB),
                    (IMAGE_SIZE, IMAGE_SIZE),
                    interpolation=cv2.INTER_AREA,
                )
                for frame in frames
            ]
        ).astype(np.float32)
        processed_frames /= 255.0
        features_input = preprocess_input(processed_frames * 255.0)

        with self._prediction_lock:
            features = self.feature_extractor.predict(
                features_input, batch_size=NUM_FRAMES, verbose=0
            )
            suspicious_probability = float(
                self.model.predict(features[np.newaxis].astype(np.float32), verbose=0)[0, 0]
            )

        label = "SUSPICIOUS" if suspicious_probability >= THRESHOLD else "NORMAL"
        confidence = (
            suspicious_probability
            if label == "SUSPICIOUS"
            else 1.0 - suspicious_probability
        )
        return {
            "label": label,
            "confidence": round(confidence, 4),
            "suspicious_probability": round(suspicious_probability, 4),
        }


def model_path() -> Path:
    configured_path = os.getenv("MODEL_PATH")
    if configured_path:
        path = Path(configured_path)
        return path if path.is_absolute() else ROOT / path

    candidates = (
        ROOT.parent / "runs" / "final_model.keras",
        ROOT / "models" / "final_model.keras",
        ROOT.parent / "runs" / "final_model.keras",
        ROOT / "models" / "final_model.keras",
    )
    return next((path for path in candidates if path.is_file()), candidates[0])


@lru_cache(maxsize=1)
def get_activity_model() -> ActivityModel:
    return ActivityModel(model_path())


def is_model_file_available() -> bool:
    return model_path().is_file()


def analyze_video(path: Path, fps: float, frame_count: int) -> dict:
    if fps <= 0 or frame_count <= 0:
        raise ValueError("Video metadata is invalid; cannot sample frames for analysis.")

    detector = get_activity_model()
    capture = cv2.VideoCapture(str(path))
    if not capture.isOpened():
        raise ValueError("Could not reopen the uploaded video for model inference.")

    frames_per_clip = max(1, round(fps * CLIP_SECONDS))
    clip_count = (frame_count + frames_per_clip - 1) // frames_per_clip
    clips = []
    try:
        for clip_index in range(clip_count):
            start_frame = clip_index * frames_per_clip
            end_frame = min(start_frame + frames_per_clip, frame_count)
            sample_indices = np.linspace(
                start_frame, end_frame - 1, NUM_FRAMES, dtype=int
            )
            sampled_frames = []
            for frame_index in sample_indices:
                capture.set(cv2.CAP_PROP_POS_FRAMES, int(frame_index))
                success, frame = capture.read()
                if not success:
                    raise ValueError(
                        f"Could not read frame {frame_index} from the uploaded video."
                    )
                sampled_frames.append(frame)

            prediction = detector.predict_clip(np.stack(sampled_frames))
            clips.append(
                {
                    "clip_index": clip_index,
                    "start_seconds": round(start_frame / fps, 2),
                    "end_seconds": round(end_frame / fps, 2),
                    **prediction,
                }
            )
    finally:
        capture.release()

    detections = [clip for clip in clips if clip["label"] == "SUSPICIOUS"]
    flagged = bool(detections)
    summary = {
        "label": "SUSPICIOUS" if flagged else "NORMAL",
        "confidence": max(
            (clip["confidence"] for clip in (detections or clips)), default=0.0
        ),
        "clips_total": len(clips),
        "clips_suspicious": len(detections),
        "clips_normal": len(clips) - len(detections),
    }
    return {"summary": summary, "clips": clips, "detections": detections}
