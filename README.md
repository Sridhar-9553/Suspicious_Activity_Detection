# Sentinel AI — Suspicious Activity Detection

[Open the Sentinel AI website](https://suspiciousactivitydetection-p3kzmupgydqmprz42hnzlg.streamlit.app/)

Sentinel AI analyzes surveillance videos in two-second intervals and classifies each interval as normal or suspicious. Its results are intended for human review and are not proof of criminal activity.

## Screenshots

<p align="center">
  <img src="ss/Screenshot%202026-10-13%20122926.png" width="48%" alt="Example interval classified as normal">
  <img src="ss/Screenshot%202026-10-13%20123248.png" width="48%" alt="Example interval classified as suspicious">
</p>
<p align="center">
  <img src="ss/Screenshot%202026-10-13%20123442.png" width="48%" alt="Night-time footage classified as suspicious">
  <img src="ss/Screenshot%202026-10-13%20123454.png" width="48%" alt="Another night-time interval classified as suspicious">
</p>

## Resources

- **Dataset:** [Video Dataset on Kaggle](https://www.kaggle.com/datasets/daudshah/video-dataset)
- **VA report (PDF):** [Open the report](https://docs.google.com/gview?embedded=1&url=https%3A%2F%2Fraw.githubusercontent.com%2FSridhar-9553%2FSuspicious_Activity_Detection%2Fmain%2FVA_report.pdf)  
  The eight-page report explains the dataset and labeling, the 16-frame feature-extraction pipeline using a frozen ResNet-50, and the bidirectional GRU with attention used to classify video clips. It also discusses threshold selection, held-out test results, and known model errors and limitations.
- **Suspicious Activity Detector (PowerPoint):** [Open the presentation](https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Fraw.githubusercontent.com%2FSridhar-9553%2FSuspicious_Activity_Detection%2Fmain%2Fcriminal_activity_detector_report.pptx)  
  The 15-slide presentation introduces the project and its temporal-classifier approach, with example surveillance-video classifications.
