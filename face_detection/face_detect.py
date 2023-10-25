# pylint: disable-all
import cv2

face_classifier = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)
video_capture = cv2.VideoCapture(0)


def detect_bounding_box(vid):
    gray_image = cv2.cvtColor(vid, cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray_image, 1.1, 5, minSize=(40, 40))
    for (x, y, w, h) in faces:
        cv2.rectangle(vid, (x, y), (x + w, y + h), (0, 255, 0), 4)
        rectangle_center = (int(x + (w / 2)), int(y + (h / 2)))
        cv2.circle(
            vid,
            ((rectangle_center)),
            2,
            (0, 255, 0),
            4,
        )
    return faces, rectangle_center


def center_normalize(center, x_max, y_max):
    center_norm = []
    center_norm.append((center[0] / x_max) - 0.5)
    center_norm.append((center[1] / y_max) - 0.5)
    return center


def move_camera(input):
    threshold = 0.2
    if input[0] > threshold:
        print("move left")
    elif input[0] < 0 - threshold:
        print("move right")


while True:

    result, video_frame = video_capture.read()  # read frames from the video
    if result is False:
        break  # terminate the loop if the frame is not read successfully

    faces, center = detect_bounding_box(
        video_frame
    )  # apply the function we created to the video frame
    center = center_normalize(center, 639, 479)
    move_camera(center)

    cv2.imshow(
        "My Face Detection Project", video_frame
    )  # display the processed frame in a window named "My Face Detection Project"

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

video_capture.release()
cv2.destroyAllWindows()
