import cv2, numpy

# Very large defaults are used for width and height as doing
# so is the most straight forward way to set the camera to
# its maximum resolution.

def stream_images_from_camera(width=100000, height=100000):
    capture = cv2.VideoCapture(0)

    capture.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    frame_count = 0

    while True:
        image_was_captured, image = capture.read()
        if not image_was_captured:
            continue
        frame_count += 1

        # Allow auto focus to complete
        if frame_count < 30:
            continue

        yield image


def get_image_from_camera(width=100000, height=100000):
    for image in stream_images_from_camera(width=width, height=height):
        return image