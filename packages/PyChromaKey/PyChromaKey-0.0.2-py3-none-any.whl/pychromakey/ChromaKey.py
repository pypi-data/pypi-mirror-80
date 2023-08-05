import cv2
import numpy as np


class MaskedImage:
    def __init__(self, mask, image):
        self.mask = mask
        self.image = image



class ChromaKey:
    def __init__(self, video_size):
        self.signal_width, self.signal_height = video_size

    def __process_foreground_image(self, frame, lower_green, upper_green):
        """"""
        img = np.copy(frame)

        # Create an image mask to change green pixels to black
        mask = cv2.inRange(img, lower_green, upper_green)

        masked_image = np.copy(img)
        masked_image[mask != 0] = [0, 0, 0]

        return MaskedImage(mask, masked_image)

    def __process_background_image(self, background_frame, mask):
        # Create another image mask to turn non-green pixels black on the background image
        background_image = cv2.cvtColor(background_frame, cv2.COLOR_BGR2RGB)

        crop_background = cv2.resize(background_image,
                                     (self.signal_width,
                                      self.signal_height))
        crop_background[mask == 0] = [0, 0, 0]
        return crop_background

    def chroma_key_image(self, frame, background_image, lower_green, upper_green, signal_width, signal_height):
        """Chroma key method."""
        if frame is None or background_image is None:
            raise RuntimeError("Foreground or background image is null.")

        cv2.normalize(frame, frame, 0, 255, cv2.NORM_MINMAX)
        foreground = self.__process_foreground_image(frame, lower_green, upper_green)
        background = self.__process_background_image(background_image, foreground.mask)

        return np.array(foreground.image + background)