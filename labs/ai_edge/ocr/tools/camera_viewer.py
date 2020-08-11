import sys, os

import cv2

grandparent_dirpath = os.path.split(os.path.split(os.path.dirname(__file__))[0])[0]
sys.path.append(grandparent_dirpath)

from ocr import capture

name = None

# Use relatively small resolution as this is only intended to setup the
# scene rather than read the text.  The cameara max resolution may be
# much larger then the monitor resolution and such setups make this tool
# difficult to use if the resolution isn't capped.
for image in capture.stream_images_from_camera(width=640, height=480):
    if name is None:
        name = "Camera Viewer"

        # This only needs to be called once
        cv2.namedWindow(name, cv2.WINDOW_AUTOSIZE)

    cv2.imshow(name, image)

    # Required by cv2 even though key presses aren't needed here
    cv2.waitKey(50)

    # This is how the close button on the window being pressed in detected and handled
    if cv2.getWindowProperty(name,cv2.WND_PROP_VISIBLE) < 1:
        cv2.destroyAllWindows()
        break
