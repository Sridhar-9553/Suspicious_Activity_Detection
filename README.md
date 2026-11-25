# Suspicious Activity Detection in Surveillance Video
### A Simple Temporal Classifier for CCTV Footage

[Open the Sentinel AI website](https://suspiciousactivitydetection-p3kzmupgydqmprz42hnzlg.streamlit.app/) - Test your own video

· [Watch the screen recording](https://github.com/Sridhar-9553/Suspicious_Activity_Detection/blob/main/ss/Screen%20Recording%202026-11-25%20191542.mp4)

## 📄 Project reports

- **VA report (PDF):** [Open the report](https://docs.google.com/gview?embedded=1&url=https%3A%2F%2Fraw.githubusercontent.com%2FSridhar-9553%2FSuspicious_Activity_Detection%2Fmain%2FVA_report.pdf) — an eight-page account of the dataset and labeling, model architecture, methodology, threshold selection, held-out test evaluation, and limitations.
- **Suspicious Activity Detector (PowerPoint):** [Open the presentation](https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Fraw.githubusercontent.com%2FSridhar-9553%2FSuspicious_Activity_Detection%2Fmain%2Fcriminal_activity_detector_report.pptx) — a 15-slide introduction to the project and its temporal-classifier approach, with example surveillance-video classifications.

## 📌 Overview

This project detects suspicious activity in surveillance videos and classifies footage as **Normal** or **Suspicious**. It combines a pretrained ResNet-50 for spatial feature extraction with a Bidirectional Gated Recurrent Unit (BiGRU) and temporal attention to learn patterns across video frames.

For model training, 16 uniformly sampled frames are converted into feature vectors and cached for efficient training. At inference, Sentinel AI evaluates video in two-second intervals and presents the classification and confidence for each interval. Results are intended for human review and are not proof of criminal activity.

## 🏗️ Proposed Architecture

The pipeline consists of the following stages:

1. **Frame sampling:** Samples 16 uniformly distributed frames from each training video.
2. **Preprocessing:** Converts frames to RGB and resizes them to 224 × 224 pixels.
3. **Feature extraction:** Uses a pretrained, frozen ResNet-50 to extract a 2048-dimensional feature vector from each frame.
4. **Feature caching:** Saves extracted features to disk to avoid repeating CNN computations during training.
5. **Temporal learning:** A bidirectional GRU models context across the frame sequence.
6. **Temporal attention:** Learns weights for frames so the classifier can focus on the most informative moments.
7. **Classification:** A fully connected head with sigmoid activation predicts the Normal/Suspicious label.

### Model components

| Component | Description |
|---|---|
| Backbone | Pretrained ResNet-50 |
| Input frames | 16 frames per training video |
| Frame resolution | 224 × 224 |
| Feature dimension | 2048 |
| Feature projection | Dense layer (256 units) |
| Temporal network | Bidirectional GRU (64 units per direction) |
| Attention | Temporal attention pooling |
| Classification | Fully connected layers + sigmoid |
| Trainable parameters | 660,738 |

## 📂 Dataset

The dataset contains 1,334 video clips split into training, validation, and testing sets. See the [Video Dataset on Kaggle](https://www.kaggle.com/datasets/daudshah/video-dataset).

| Dataset split | Total videos | Normal | Suspicious |
|---|---:|---:|---:|
| Training | 940 | 380 | 560 |
| Validation | 194 | 91 | 103 |
| Testing | 200 | 143 | 57 |
| **Total** | **1,334** | **614** | **720** |

Suspicious categories include abuse, arrest, arson, assault, burglary, explosion, fighting, road accidents, robbery, shooting, shoplifting, stealing, and vandalism. Normal activities include walking, sitting, standing, clapping, and other routine activities.

## ⚙️ Training configuration

| Parameter | Value |
|---|---|
| Framework | TensorFlow 2.21.0 / Keras |
| Feature extractor | Frozen ResNet-50 |
| Temporal model | Bidirectional GRU |
| Loss function | Focal Loss |
| Optimizer | Adam |
| Initial learning rate | 0.001 |
| Batch size | 32 |
| Maximum epochs | 80 |
| Early stopping patience | 6 |
| Dropout | 0.4 and 0.6 |
| Decision threshold | 0.705 |

The decision threshold is selected using macro F1-score on the validation dataset to balance performance across the two classes.

## 📊 Experimental results

The model's reported performance on the held-out test dataset is:

| Evaluation metric | Result |
|---|---:|
| Test accuracy | **90.50%** |
| Macro F1-score | **0.890** |
| Normal class F1-score | 0.931 |
| Suspicious class F1-score | 0.848 |
| Suspicious activity recall | **93.00%** |
| Suspicious activity precision | 77.90% |

### Confusion matrix

| Actual / predicted | Normal | Suspicious |
|---|---:|---:|
| Normal | 128 | 15 |
| Suspicious | 4 | 53 |

The model correctly classified 53 of the 57 suspicious clips in this test split. These evaluation results do not guarantee equivalent performance on other footage.

## 🖼️ Visual results

The inference pipeline displays a predicted category and confidence score on video frames. Green indicates a Normal prediction; red indicates a Suspicious prediction.

<p align="center">
  <img src="ss/Screenshot%202026-10-13%20122926.png" width="48%" alt="Example interval classified as normal">
  <img src="ss/Screenshot%202026-10-13%20123248.png" width="48%" alt="Example interval classified as suspicious">
</p>
<p align="center">
  <img src="ss/Screenshot%202026-10-13%20123442.png" width="48%" alt="Night-time footage classified as suspicious">
  <img src="ss/Screenshot%202026-10-13%20123454.png" width="48%" alt="Another night-time interval classified as suspicious">
</p>

## 🛠️ Technologies used

- Python, TensorFlow, Keras, OpenCV, NumPy, and scikit-learn
- ResNet-50, Bidirectional GRU, and temporal attention

## ✨ Key features

- Spatial feature extraction with pretrained ResNet-50.
- Temporal sequence modeling with a bidirectional GRU and attention.
- Feature caching for more efficient training.
- Focal loss for class imbalance.
- Validation-based decision-threshold selection.
- Video inference with per-interval predictions and confidence scores.

## ⚠️ Limitations

- The training dataset is relatively small, creating a risk of overfitting.
- Complex motion in normal footage can produce false alarms.
- Differences in source resolution between normal and suspicious clips may encourage shortcut learning.
- Sampling a limited number of frames may miss subtle or brief events.
- Model results can be wrong and require human review; they are not proof of criminal activity.

## 🚀 Future work

- Train and evaluate with larger, more diverse surveillance datasets.
- Use resolution-matched evaluation to investigate shortcut learning.
- Compare against established video anomaly-detection approaches.
- Explore two-stream appearance and motion models or temporal transformers.
- Improve temporal sampling to capture subtle activity.

## 👨‍💻 Contributors

- **Anurag Choudhury**
- **Kolli Sridhar**
- **Harsha Vardhan**

---

**Project title:** Suspicious Activity Detection in Surveillance Video  
**Approach:** ResNet-50 + Bidirectional GRU + Temporal Attention  
**Task:** Binary video classification (Normal / Suspicious)
