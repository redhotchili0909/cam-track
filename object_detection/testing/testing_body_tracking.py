import cv2
from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator
import torch
import numpy as np
model = YOLO()
cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, frame = cap.read()
    results = model.predict(frame, verbose=False)

    for r in results:
        annotator = Annotator(frame)

        boxes = r.boxes
        for box in boxes:
            box_coord = box.xyxy[0]  # get box coordinates in (top, left, bottom, right) format
            c = box.cls
            annotator.box_label(box_coord, model.names[int(c)])
            if model.names[int(c)] == "person":
                box_coord = torch.Tensor.cpu(box_coord)
                box_coord = torch.Tensor.numpy(box_coord)
                print(box_coord)
                

    annotated_frame = annotator.result()
    cv2.imshow("YOLO", annotated_frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
cap.release()
cv2.destroyAllWindows()