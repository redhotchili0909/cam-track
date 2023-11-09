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
                print(box_coord[0])

                

    annotated_frame = annotator.result()
    center_x = (box_coord[0] + box_coord[2])/2
    center_y = (box_coord[1] + box_coord[3])/2
    annotated_frame = cv2.circle(annotated_frame, (int(center_x), int(center_y)), radius=0, color=(0, 0, 255), thickness=10 )
    cv2.imshow("YOLO", annotated_frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
cap.release()
cv2.destroyAllWindows()