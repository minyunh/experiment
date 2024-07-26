
import torch

# Model
model = torch.hub.load("ultralytics/yolov5", 'custom', path='best.pt')

# Images
img = "test.jpg"  # or file, Path, PIL, OpenCV, numpy, list

# Inference
results = model(img)

# Results
results.print()  # or .show(), .save(), .crop(), .pandas(), etc.
results.show()
