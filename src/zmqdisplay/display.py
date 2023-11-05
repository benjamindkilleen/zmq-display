import numpy as np
import cv2
import screeninfo
import multiprocessing as mp
import logging
import zmq

from .container import ImageContainer

log = logging.getLogger(__name__)


def resize(image: np.ndarray, width: int, height: int) -> np.ndarray:
    """Resize a numpy array image to the given width and height.

    Maintain the aspect ratio of the image and pad extra space with 0s."""

    h, w, _ = image.shape

    if w / h > width / height:
        # Image is wider than target
        new_w = width
        new_h = int(width * h / w)
        pad_top = int((height - new_h) / 2)
        pad_bottom = height - new_h - pad_top
        pad_left = 0
        pad_right = 0
    else:
        # Image is taller than target
        new_w = int(height * w / h)
        new_h = height
        pad_top = 0
        pad_bottom = 0
        pad_left = int((width - new_w) / 2)
        pad_right = width - new_w - pad_left

    image = cv2.resize(image, (new_w, new_h))
    image = cv2.copyMakeBorder(
        image, pad_top, pad_bottom, pad_left, pad_right, cv2.BORDER_CONSTANT, value=0
    )
    return image


class ImageDisplay(mp.Process):
    """A class for sending and receiving images over zmq.

    Images are encoded"""

    def __init__(self, host: str, port: int = 7896) -> None:
        super().__init__()
        self.host = host
        self.port = port
        self._running = mp.Event()

    def run(self):
        screen = screeninfo.get_monitors()[-1]
        width, height = screen.width, screen.height
        window_name = "Image"
        cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
        cv2.moveWindow(window_name, screen.x - 1, screen.y - 1)

        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.SUB)
        self.socket.connect(f"tcp://{self.host}:{self.port}")
        self.socket.setsockopt_string(zmq.SUBSCRIBE, np.unicode(""))

        self._running.set()

        while self._running.is_set():
            try:
                image_json = self.socket.recv_json()
                image_container = ImageContainer.from_dict(image_json)
                image = image_container.data
                image = resize(image, width, height)
                cv2.imshow(window_name, image)
                cv2.waitKey(5)
            except KeyboardInterrupt:
                break

        cv2.destroyAllWindows()

    def stop(self):
        self._running.clear()
