# pylint: disable-all
# Script for running the Raspberry Pi 4 Camera and Arduino Serial Communication
import cv2
import numpy as np
import serial
from picamera2 import Picamera2, Preview

# Load Cascade Classifier Files
face_classifier = cv2.CascadeClassifier("models/haarcascade_frontalface_default.xml")
body_classifier = cv2.CascadeClassifier("models/haarcascade_fullbody.xml")
upper_classifier = cv2.CascadeClassifier("models/haarcascade_upperbody.xml")

# Start Capturing Video
picam2 = Picamera2()
picam2.start()

# Define the width & height of the video frame
frame_width = 600
frame_height = 400

# Connect to Ardunio Serial Port
ser = serial.Serial("/dev/ttyACM0", 9600, timeout=1)
ser.reset_input_buffer()


class ObjectDetect:
    """
    Object detection class.

    This class encapsulates object detection functionality, including finding the closest object
    within the frame, drawing bounding boxes, and calculating center coordinates.

    Args:
        classifier: A Haar Cascade classifier for object detection.

    Methods:
        - detect_bounding_box(frame): Detects the closest object's bounding box in the given frame
          and returns the bounding box coordinates and center.
        - show_bounds(object, frame): Draws a bounding box and center point for the given object
          on the frame.
    """

    def __init__(self, classifer):
        self.classifier = classifer

    def detect_bounding_box(self, frame):
        gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        objects = self.classifier.detectMultiScale(gray_image, 1.1, 5, minSize=(40, 40))
        closest_object = 0
        max_box_area = 0
        max_object_idx = 0
        cur_box_area = 0

        if isinstance(objects, np.ndarray):
            for idx, object in enumerate(objects):
                cur_box_area = object[2] * object[3]
                if cur_box_area > max_box_area:
                    max_box_area = cur_box_area
                    max_object_idx = idx

            closest_object = objects[max_object_idx]
            x, y, w, h = closest_object

            # Display rectangle of the closest object
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 4)
            rectangle_center = (int(x + (w / 2)), int(y + (h / 2)))

            # Display rectangle center point
            cv2.circle(
                frame,
                ((rectangle_center)),
                2,
                (0, 255, 0),
                4,
            )
        else:
            # If box is out of bounds, return an array of 0s
            closest_object = np.ndarray([0, 0, 0, 0])
            rectangle_center = (0, 0)
        return closest_object, rectangle_center


def resize_frame(frame: np.ndarray, width, height):
    """
    Resize a frame to a specified width and height.

    Args:
        frame (numpy.ndarray): The input frame.
        width (int): The target width for the frame.
        height (int): The target height for the frame.

    Returns:
        numpy.ndarray: The resized frame.
    """
    return cv2.resize(frame, (width, height))


def center_normalize(center, x_max, y_max):
    """
    Normalize the center coordinates to be within the range [-0.5, 0.5].

    Args:
        center (tuple): The center coordinates (x, y).
        x_max (int): The maximum x-coordinate (frame width).
        y_max (int): The maximum y-coordinate (frame height).

    Returns:
        tuple: Normalized center coordinates (x_norm, y_norm).
    """
    center_norm = []
    center_norm.append((center[0] / x_max) - 0.5)
    center_norm.append((center[1] / y_max) - 0.5)
    return center


def move_camera(input):
    """
    Calculate the movement needed to center an object.

    Args:
        input (tuple): The center coordinates of an object (x, y).

    Returns:
        float: The movement required to center the object, with a threshold to prevent small
        movements from being considered.
    """
    frame_center = frame_width / 2
    move = input[0] - frame_center
    threshold = 50
    if abs(move) < threshold:
        move = 0
        print("move left")
    elif input[0] < threshold and input[0] > 0:
        print("move right")
    elif input[0] == 0:
        print("out of frame")
    return move


while True:
    # Read data from video capture
    frame = picam2.capture_array("main")
    if frame is False:
        break
    # Change color and size of frame
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    frame = resize_frame(frame, frame_width, frame_height)

    # Assign an object classifier
    # - face_classifier: face
    # - body_classifier: full-body
    # - upper_classifier: upper-body
    detection = ObjectDetect(body_classifier)
    object, center = detection.detect_bounding_box(frame)

    center = center_normalize(center, frame_width, frame_height)

    move_command = str(move_camera(center))
    move_command = move_command + "\n"
    print(f"from pi: {move_command}")
    ser.write(move_command.encode("utf-8"))
    line = ser.readline().decode("utf-8").rstrip()
    print(f"from arduino: {line}")

    # Make sure to comment when running the script without display output
    cv2.imshow("My Face Detection Project", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
