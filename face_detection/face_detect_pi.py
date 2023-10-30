# pylint: disable-all
import cv2
import numpy as np
import serial
from picamera2 import Picamera2, Preview
face_classifier = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
picam2 = Picamera2()
picam2.start()

frame_width = 1200
frame_height = 800

def resize_frame(frame, width, height):
    return cv2.resize(frame, (width, height))

def detect_bounding_box(vid):
    gray_image = cv2.cvtColor(vid, cv2.COLOR_RGB2GRAY)
    faces = face_classifier.detectMultiScale(gray_image, 1.1, 5, minSize=(40, 40))
    closest_face = 0
    max_box_area = 0
    max_face_idx = 0
    cur_box_area = 0
    if isinstance(faces, np.ndarray):
        for idx, face in enumerate(faces):
            cur_box_area = face[2] * face[3]
            # find biggest box area when camera picks up multiple faces
            # to only track the closest face~
            if cur_box_area > max_box_area:
                max_box_area = cur_box_area
                max_face_idx = idx
        closest_face = faces[max_face_idx]
        x = closest_face[0]
        y = closest_face[1]
        w = closest_face[2]
        h = closest_face[3]
        # display rectange of only closest face
        cv2.rectangle(vid, (x, y), (x + w, y + h), (0, 255, 0), 4)
        rectangle_center = (int(x + (w / 2)), int(y + (h / 2)))
        cv2.circle(
            vid,
            ((rectangle_center)),
            2,
            (0, 255, 0),
            4,
        )
    else:

        # if box is out of bounds, just set everything to 0s so it doesn't crash lol
        closest_face = np.ndarray([0, 0, 0, 0])
        rectangle_center = (0, 0)
    return closest_face, rectangle_center

    # cv2.imshow(
    #     "My Face Detection Project", array
    # )  # display the processed frame in a window named "My Face Detection Project"
def center_normalize(center, x_max, y_max):
    center_norm = []
    center_norm.append((center[0] / x_max) - 0.5)
    center_norm.append((center[1] / y_max) - 0.5)
    return center


def move_camera(input):
    # return how far center of rectangle is from the middle of the screen
    # TODO: send this number to arduino over serial
    threshold = frame_width / 2
    move = input[0] - threshold
    if input[0] > threshold:
        print("move left")
    elif input[0] < threshold and input[0] > 0:
        print("move right")
    elif input[0] == 0:
        print("out of frame")
    return move

if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    ser.reset_input_buffer()

while True:
    array = picam2.capture_array("main")
    array = cv2.cvtColor(array,cv2.COLOR_RGB2BGR)
    if array is False:
        break  # terminate the loop if the frame is not read successfully
    array = resize_frame(array,frame_width,frame_height)
    faces, center = detect_bounding_box(
        array
    )  # apply the function we created to the video frame
    center = center_normalize(center, frame_width, frame_height)
    move_command = str(move_camera(center))
    print(f"from pi: {move_command}")
    ser.write(move_command.encode('utf-8'))
    line = ser.readline().decode('utf-8').rstrip()
    print(f"from arduino: {line}")

    # cv2.imshow(
    #     "My Face Detection Project", array
    # )  # display the processed frame in a window named "My Face Detection Project"
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
