Suspicious Activity Detection in Surveillance Video
A lightweight temporal classifier that flags suspicious activity in short CCTV clips. Each clip is reduced to 16 frames, embedded once with a frozen ResNet-50, and classified by a small BiGRU + attention head. The whole trainable model has ~660K parameters and trains in about one second per epoch on CPU thanks to feature caching.

Overview
Security cameras generate far more footage than any human team can review. This project builds a binary classifier that labels a clip as Normal or Suspicious, so operators can focus on flagged moments instead of scrubbing through hours of video.

Pipeline: Video clip → 16 evenly-spaced frames (224×224) → frozen ResNet-50 (2048-D per frame) → cached features → LayerNorm → Dense 256 + Dropout → BiGRU (64+64) → Temporal Attention → Dense 64 + Dropout → sigmoid → threshold → Normal/Suspicious

The expensive part (feature extraction) runs once and is cached to disk. Everything after that trains on saved feature tensors.

Key Design Choices
Frozen backbone — ResNet-50 (ImageNet weights) is never retrained. Prevents overfitting and keeps training fast.

Feature caching — 1,334 clips extracted in ~23 minutes on CPU; training then takes ~1 s/epoch.

BiGRU + attention — reads the frame sequence in both directions and learns which frames matter, instead of naive averaging.

Focal Loss (α = 0.6, γ = 2.0) — concentrates training on hard examples so the model doesn't lazily predict "normal".

Fair threshold selection — 181 thresholds tested on validation; the one maximizing macro F1 is chosen (θ* = 0.705), treating both classes equally regardless of class balance.

Dataset
Videos are organized into train / validation / test splits with plain-text manifest files. Labels are derived from filenames (activity category prefix).

Split	Videos	Normal	Suspicious
Train	940	380 (40.4%)	560 (59.6%)
Validation	194	91 (46.9%)	103 (53.1%)
Test	200	143 (71.5%)	57 (28.5%)
Normal: clapping, meet-and-split, sitting, standing-still, walking (incl. walking-while-using-phone / reading), normal videos.

Suspicious: abuse, arrest, arson, assault, burglary, explosion, fighting, road accidents, robbery, shooting, shoplifting, stealing, vandalism.

The test set is deliberately mostly normal — a harder, more realistic distribution than training.
