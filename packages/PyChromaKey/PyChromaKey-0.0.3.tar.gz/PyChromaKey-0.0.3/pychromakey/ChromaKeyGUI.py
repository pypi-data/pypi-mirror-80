import cv2
import numpy as np


def do_nothing(x):
    """Do nothing"""
    pass


class ChromaKeyGUIException(Exception):
    pass


class ChromaKeyGUI:
    def __init__(self, preview, lower_green=([0, 100, 0]), upper_green=([80, 255, 40]), show_preview=True):
        self.show_preview = preview
        self.lower_green = lower_green
        self.upper_green = upper_green
        self.show_preview = show_preview

    def __enter__(self):
        # Define GUI elements
        self.preview_window = 'preview'
        self.control_window = 'control'

        cv2.namedWindow(self.control_window)

        if self.show_preview:
            cv2.namedWindow(self.preview_window)

        # create trackbars for color change
        cv2.createTrackbar('R_Min', self.control_window, self.lower_green[0], 255, do_nothing)
        cv2.createTrackbar('G_Min', self.control_window, self.lower_green[1], 255, do_nothing)
        cv2.createTrackbar('B_Min', self.control_window, self.lower_green[2], 255, do_nothing)

        cv2.createTrackbar('R_Max', self.control_window, self.upper_green[0], 255, do_nothing)
        cv2.createTrackbar('G_Max', self.control_window, self.upper_green[1], 255, do_nothing)
        cv2.createTrackbar('B_Max', self.control_window, self.upper_green[2], 255, do_nothing)

        return self

    def update_values(self):
        """Get trackbar positions for RGB balance"""
        self.lower_green = np.array([cv2.getTrackbarPos('R_Min', self.control_window),
                                     cv2.getTrackbarPos('G_Min', self.control_window),
                                     cv2.getTrackbarPos('B_Min', self.control_window)])

        self.upper_green = np.array([cv2.getTrackbarPos('R_Max', self.control_window),
                                     cv2.getTrackbarPos('G_Max', self.control_window),
                                     cv2.getTrackbarPos('B_Max', self.control_window)])

    def update_preview(self, new_frame):
        """Update image in preview window"""
        if not self.show_preview:
            pass
        else:
            cv2.imshow(self.preview_window, new_frame)

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Cleanup
        cv2.destroyWindow(self.control_window)
        cv2.destroyWindow(self.preview_window)
