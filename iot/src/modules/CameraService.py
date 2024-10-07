import cv2
import numpy
import picamera2


class CameraService:
    def __init__(self):
        self.camera = cv2.VideoCapture(0)

    def capture_image(self) -> numpy.ndarray:
        """Captures an image from Raspberry Pi camera using OpenCV."""
        ret, frame = self.camera.read()
        if not ret:
            print("Failed to capture image.")
            return None
        self.camera.release()
        return frame

    def dummy_image(self) -> numpy.ndarray:
        image = cv2.imread(
            "/home/raspberrypi/Projects/solar/SolarSense/iot/Imgdirty_5_1.jpg",
            cv2.IMREAD_COLOR,
        )
        return image
