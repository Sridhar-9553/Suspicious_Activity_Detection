
# Suspicious Activity Detection in Surveillance Video
### A Simple Temporal Classifier for CCTV Footage

## 📌 Overview

This project focuses on detecting suspicious activities in surveillance videos using deep learning. It aims to classify video clips into two categories: **Normal** and **Suspicious**.

The proposed approach combines a pretrained ResNet-50 model for spatial feature extraction with a Bidirectional Gated Recurrent Unit (BiGRU) and a Temporal Attention mechanism to learn important patterns across video frames.

Instead of processing entire videos directly, the system extracts features from 16 uniformly sampled frames per video and stores them for efficient training. These features are then passed through a lightweight temporal classification network to predict suspicious activities.

## 🏗️ Proposed Architecture

The overall pipeline consists of the following stages:

1. **Frame Sampling:** Extracts 16 uniformly distributed frames from each input video.
2. **Preprocessing:** Converts frames to RGB format and resizes them to 224 × 224 pixels.
3. **Feature Extraction:** Uses a pretrained and frozen ResNet-50 network to extract 2048-dimensional feature vectors from each frame.
4. **Feature Caching:** Stores extracted features on disk to avoid repeated CNN computations during training.
5. **Temporal Learning:** A Bidirectional GRU captures temporal dependencies between consecutive frame features.
6. **Temporal Attention:** Assigns importance weights to different frames, allowing the model to focus on potentially suspicious activities.
7. **Classification:** A fully connected classification head with sigmoid activation predicts the final Normal/Suspicious label.

### Model Components

| Component | Description |
|---|---|
| Backbone | Pretrained ResNet-50 |
| Input Frames | 16 frames per video |
| Frame Resolution | 224 × 224 |
| Feature Dimension | 2048 |
| Feature Projection | Dense layer (256 units) |
| Temporal Network | Bidirectional GRU (64 units per direction) |
| Attention | Temporal Attention Pooling |
| Classification | Fully Connected Layers + Sigmoid |
| Trainable Parameters | 660,738 |

## 📂 Dataset

The dataset consists of surveillance video clips representing normal and suspicious activities.

The dataset contains 1,334 videos divided into training, validation, and testing sets.

| Dataset Split | Total Videos | Normal | Suspicious |
|---|---:|---:|---:|
| Training | 940 | 380 | 560 |
| Validation | 194 | 91 | 103 |
| Testing | 200 | 143 | 57 |
| **Total** | **1,334** | **614** | **720** |

### Suspicious Activities

The suspicious category includes activities such as:

- Abuse
- Arrest
- Arson
- Assault
- Burglary
- Explosion
- Fighting
- Road Accidents
- Robbery
- Shooting
- Shoplifting
- Stealing
- Vandalism

Normal activities include walking, sitting, standing, clapping, and other routine activities.

## ⚙️ Training Configuration

| Parameter | Value |
|---|---|
| Framework | TensorFlow 2.21.0 / Keras |
| Programming Language | Python |
| Feature Extractor | ResNet-50 (Frozen) |
| Temporal Model | Bidirectional GRU |
| Loss Function | Focal Loss |
| Optimizer | Adam |
| Initial Learning Rate | 0.001 |
| Batch Size | 32 |
| Maximum Epochs | 80 |
| Early Stopping Patience | 6 |
| Dropout | 0.4 and 0.6 |
| Decision Threshold | 0.705 |

The decision threshold is optimized using the macro F1-score on the validation dataset to balance the classification performance of both classes.

## 📊 Experimental Results

The proposed model achieved the following performance on the held-out test dataset:

| Evaluation Metric | Result |
|---|---:|
| Test Accuracy | **90.50%** |
| Macro F1-Score | **0.890** |
| Normal Class F1-Score | 0.931 |
| Suspicious Class F1-Score | 0.848 |
| Suspicious Activity Recall | **93.00%** |
| Suspicious Activity Precision | 77.90% |

### Confusion Matrix

| Actual / Predicted | Normal | Suspicious |
|---|---:|---:|
| Normal | 128 | 15 |
| Suspicious | 4 | 53 |

The model correctly identifies 53 out of 57 suspicious video clips, achieving a suspicious activity recall of 93%.

## 🖼️ Visual Results

The inference pipeline generates annotated video frames displaying the predicted activity category and corresponding confidence score.

- Green indicator: Normal activity.
- Red indicator: Suspicious activity.

These visual predictions help interpret the model's output on surveillance footage.

## 🛠️ Technologies Used

- Python
- TensorFlow
- Keras
- OpenCV
- NumPy
- Scikit-learn
- Matplotlib
- ResNet-50
- Bidirectional GRU
- Temporal Attention Mechanism

## ✨ Key Features

- Deep learning-based suspicious activity detection.
- Spatial feature extraction using pretrained ResNet-50.
- Temporal sequence modelling using Bidirectional GRU.
- Attention-based learning to identify important video frames.
- Feature caching for computational efficiency.
- Focal Loss for handling class imbalance.
- Validation-based decision threshold optimization.
- Annotated video inference with prediction labels and confidence scores.

## ⚠️ Limitations

Despite achieving promising results, the current approach has some limitations:

- Overfitting due to the relatively small training dataset.
- False alarms on normal videos containing complex movements.
- Potential shortcut learning due to differences in video resolution between normal and suspicious footage.
- Limited temporal information from sampling only 16 frames per video.

## 🚀 Future Work

Potential improvements include:

- Training with larger and more diverse surveillance datasets.
- Resolution-matched evaluation to reduce shortcut learning.
- Comparing performance with established video anomaly detection approaches.
- Exploring two-stream appearance and motion-based networks.
- Investigating transformer-based temporal architectures.
- Improving temporal feature extraction to capture subtle suspicious activities.

## 👨‍💻 Contributors

- **Anurag Choudhury**
- **Kolli Sridhar**
- **Harsha Vardhan**

---

**Project Title:** Suspicious Activity Detection in Surveillance Video

**Approach:** ResNet-50 + Bidirectional GRU + Temporal Attention

**Task:** Binary Video Classification (Normal / Suspicious)
