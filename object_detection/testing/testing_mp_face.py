"""Main scripts to run face detector through MediaPipe."""

import argparse
import sys
import time

import cv2
import mediapipe as mp
import numpy as np

from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# Global variables to calculate FPS
COUNTER, FPS = 0, 0
START_TIME = time.time()
DETECTION_RESULT = None


def run(
    model: str,
    min_detection_confidence: float,
    min_suppression_threshold: float,
    camera_id: int,
    width: int,
    height: int,
) -> None:
    """Continuously run inference on images acquired from the camera.

    Args:
      model: Name of the TFLite face detection model.
      min_detection_confidence: The minimum confidence score for the face
        detection to be considered successful.
      min_suppression_threshold: The minimum non-maximum-suppression threshold for
        face detection to be considered overlapped.
      camera_id: The camera id to be passed to OpenCV.
      width: The width of the frame captured from the camera.
      height: The height of the frame captured from the camera.
    """

    # Start capturing video input from the camera
    cap = cv2.VideoCapture(camera_id)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    # Visualization parameters
    row_size = 50  # pixels
    left_margin = 24  # pixels
    text_color = (0, 0, 0)  # black
    font_size = 1
    font_thickness = 1
    fps_avg_frame_count = 10

    def save_result(
        result: vision.FaceDetectorResult,
        unused_output_image: mp.Image,
        timestamp_ms: int,
    ):
        global FPS, COUNTER, START_TIME, DETECTION_RESULT

        # Calculate the FPS
        if COUNTER % fps_avg_frame_count == 0:
            FPS = fps_avg_frame_count / (time.time() - START_TIME)
            START_TIME = time.time()

        DETECTION_RESULT = result
        COUNTER += 1

    # Initialize the face detection model
    base_options = python.BaseOptions(model_asset_path=model)
    options = vision.FaceDetectorOptions(
        base_options=base_options,
        running_mode=vision.RunningMode.LIVE_STREAM,
        min_detection_confidence=min_detection_confidence,
        min_suppression_threshold=min_suppression_threshold,
        result_callback=save_result,
    )
    detector = vision.FaceDetector.create_from_options(options)

    # Continuously capture images from the camera and run inference
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            sys.exit(
                "ERROR: Unable to read from webcam. Please verify your webcam settings."
            )

        image = cv2.flip(image, 1)

        # Convert the image from BGR to RGB as required by the TFLite model.
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_image)

        # Run face detection using the model.
        detector.detect_async(mp_image, time.time_ns() // 1_000_000)

        # Show the FPS
        fps_text = "FPS = {:.1f}".format(FPS)
        text_location = (left_margin, row_size)
        current_frame = image
        cv2.putText(
            current_frame,
            fps_text,
            text_location,
            cv2.FONT_HERSHEY_DUPLEX,
            font_size,
            text_color,
            font_thickness,
            cv2.LINE_AA,
        )

        if DETECTION_RESULT:
            # print(DETECTION_RESULT)
            current_frame = visualize(current_frame, DETECTION_RESULT)

        cv2.imshow("face_detection", current_frame)

        # Stop the program if the ESC key is pressed.
        if cv2.waitKey(1) == 27:
            break

    detector.close()
    cap.release()
    cv2.destroyAllWindows()


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "--model",
        help="Path of the face detection model.",
        required=False,
        default="object_detection/models/mp/shortrange_detector.tflite",
    )
    parser.add_argument(
        "--minDetectionConfidence",
        help="The minimum confidence score for the face detection to be "
        "considered successful..",
        required=False,
        type=float,
        default=0.5,
    )
    parser.add_argument(
        "--minSuppressionThreshold",
        help="The minimum non-maximum-suppression threshold for face detection "
        "to be considered overlapped.",
        required=False,
        type=float,
        default=0.5,
    )
    # Finding the camera ID can be very reliant on platform-dependent methods.
    # One common approach is to use the fact that camera IDs are usually indexed sequentially by the OS, starting from 0.
    # Here, we use OpenCV and create a VideoCapture object for each potential ID with 'cap = cv2.VideoCapture(i)'.
    # If 'cap' is None or not 'cap.isOpened()', it indicates the camera ID is not available.
    parser.add_argument(
        "--cameraId", help="Id of camera.", required=False, type=int, default=0
    )
    parser.add_argument(
        "--frameWidth",
        help="Width of frame to capture from camera.",
        required=False,
        type=int,
        default=1280,
    )
    parser.add_argument(
        "--frameHeight",
        help="Height of frame to capture from camera.",
        required=False,
        type=int,
        default=720,
    )
    args = parser.parse_args()

    run(
        args.model,
        args.minDetectionConfidence,
        args.minSuppressionThreshold,
        int(args.cameraId),
        args.frameWidth,
        args.frameHeight,
    )


MARGIN = 10  # pixels
ROW_SIZE = 30  # pixels
FONT_SIZE = 1
FONT_THICKNESS = 1
TEXT_COLOR = (0, 0, 0)  # black


def visualize(image, detection_result) -> np.ndarray:
    """Draws bounding boxes on the input image and return it.
    Args:
      image: The input RGB image.
      detection_result: The list of all "Detection" entities to be visualized.
    Returns:
      Image with bounding boxes.
    """
    for detection in detection_result.detections:
        # Draw bounding_box
        bbox = detection.bounding_box
        start_point = bbox.origin_x, bbox.origin_y
        end_point = bbox.origin_x + bbox.width, bbox.origin_y + bbox.height
        # Use the orange color for high visibility.
        cv2.rectangle(image, start_point, end_point, (0, 165, 255), 3)

        # Draw label and score
        category = detection.categories[0]
        category_name = (
            category.category_name if category.category_name is not None else ""
        )
        probability = round(category.score, 2)
        result_text = category_name + " (" + str(probability) + ")"
        text_location = (MARGIN + bbox.origin_x, MARGIN + ROW_SIZE + bbox.origin_y)
        cv2.putText(
            image,
            result_text,
            text_location,
            cv2.FONT_HERSHEY_DUPLEX,
            FONT_SIZE,
            TEXT_COLOR,
            FONT_THICKNESS,
            cv2.LINE_AA,
        )

    return image


if __name__ == "__main__":
    main()
