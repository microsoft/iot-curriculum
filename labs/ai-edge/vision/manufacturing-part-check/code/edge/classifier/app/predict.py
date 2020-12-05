# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

from urllib.request import urlopen
from datetime import datetime
import tensorflow as tf

from PIL import Image
import numpy as np
import sys

try:
    import cv2
    use_opencv = True
    print("Using OpenCV resizing...")
except:
    use_opencv = False
    print("Using CVS resizing...")

filename = 'model.pb'
labels_filename = 'labels.txt'

network_input_size = 0

output_layer = 'loss:0'
input_node = 'Placeholder:0'

graph_def = tf.compat.v1.GraphDef()
labels = []


def initialize():
    print('Loading model...',end=''),
    with open(filename, 'rb') as f:
        graph_def.ParseFromString(f.read())
        tf.import_graph_def(graph_def, name='')

    # Retrieving 'network_input_size' from shape of 'input_node'
    with tf.compat.v1.Session() as sess:
        input_tensor_shape = sess.graph.get_tensor_by_name(input_node).shape.as_list()
        
    assert len(input_tensor_shape) == 4
    assert input_tensor_shape[1] == input_tensor_shape[2]

    global network_input_size
    network_input_size = input_tensor_shape[1]
   
    print('Success!')
    print('Loading labels...', end='')
    with open(labels_filename, 'rt') as lf:
        global labels
        labels = [l.strip() for l in lf.readlines()]
    print(len(labels), 'found. Success!')


def log_msg(msg):
    print("{}: {}".format(datetime.now(),msg))


def extract_bilinear_pixel(img, x, y, ratio, xOrigin, yOrigin):
    """
    Custom implementation of bilinear interpolation when opencv is not available
    img: numpy source image array
    x,y: target pixel coordinates
    ratio: scaling factor
    xOrigin, yOrigin: source image offset
    returns interpolated pixel value (RGB)
    """
    xDelta = (x + 0.5) * ratio - 0.5
    x0 = int(xDelta)
    xDelta -= x0
    x0 += xOrigin
    if x0 < 0:
        x0 = 0;
        x1 = 0;
        xDelta = 0.0;
    elif x0 >= img.shape[1]-1:
        x0 = img.shape[1]-1;
        x1 = img.shape[1]-1;
        xDelta = 0.0;
    else:
        x1 = x0 + 1;
    
    yDelta = (y + 0.5) * ratio - 0.5
    y0 = int(yDelta)
    yDelta -= y0
    y0 += yOrigin
    if y0 < 0:
        y0 = 0;
        y1 = 0;
        yDelta = 0.0;
    elif y0 >= img.shape[0]-1:
        y0 = img.shape[0]-1;
        y1 = img.shape[0]-1;
        yDelta = 0.0;
    else:
        y1 = y0 + 1;

    #Get pixels in four corners
    bl = img[y0, x0]
    br = img[y0, x1]
    tl = img[y1, x0]
    tr = img[y1, x1]
    #Calculate interpolation
    b = xDelta * br + (1. - xDelta) * bl
    t = xDelta * tr + (1. - xDelta) * tl
    pixel = yDelta * t + (1. - yDelta) * b
    return pixel


def extract_and_resize(img, targetSize):
    """
    resize and cropn when opencv is not available
    img: input image numpy array
    targetSize: output size
    returns resized and cropped image
    """
    determinant = img.shape[1] * targetSize[0] - img.shape[0] * targetSize[1]
    if determinant < 0:
        ratio = float(img.shape[1]) / float(targetSize[1])
        xOrigin = 0
        yOrigin = int(0.5 * (img.shape[0] - ratio * targetSize[0]))
    elif determinant > 0:
        ratio = float(img.shape[0]) / float(targetSize[0])
        xOrigin = int(0.5 * (img.shape[1] - ratio * targetSize[1]))
        yOrigin = 0
    else:
        ratio = float(img.shape[0]) / float(targetSize[0])
        xOrigin = 0
        yOrigin = 0
    resize_image = np.empty((targetSize[0], targetSize[1], img.shape[2]), dtype=np.float32)
    for y in range(targetSize[0]):
        for x in range(targetSize[1]):
            resize_image[y, x] = extract_bilinear_pixel(img, x, y, ratio, xOrigin, yOrigin)
    return resize_image


def extract_and_resize_to_256_square(image):
    """
    extracts image central square crop and resizes it to 256x256
    image: input image numpy array
    returns resized 256x256 central crop as numpy array
    """
    h, w = image.shape[:2]
    log_msg("crop_center: " + str(w) + "x" + str(h) +" and resize to " + str(256) + "x" + str(256))
    if use_opencv:
        min_size = min(h, w)
        image = crop_center(image, min_size, min_size)
        return cv2.resize(image, (256, 256), interpolation = cv2.INTER_LINEAR)
    else:
        return extract_and_resize(image, (256, 256))


def crop_center(img,cropx,cropy):
    """
    extracts central crop
    img: input image numpy array
    cropx, cropy: crop size
    returns central crop as numpy array
    """
    h, w = img.shape[:2]
    startx = max(0, w//2-(cropx//2))
    starty = max(0, h//2-(cropy//2))
    log_msg("crop_center: " + str(w) + "x" + str(h) +" to " + str(cropx) + "x" + str(cropy))
    return img[starty:starty+cropy, startx:startx+cropx]


def resize_down_to_1600_max_dim(image):
    """
    resized image to 1600px in max dimension if image exceeds 1600 by width or height
    image: input image numpy array
    returns downsized image
    """
    w,h = image.size
    if h < 1600 and w < 1600:
        return image

    new_size = (1600 * w // h, 1600) if (h > w) else (1600, 1600 * h // w)
    log_msg("resize: " + str(w) + "x" + str(h) + " to " + str(new_size[0]) + "x" + str(new_size[1]))
    
    if use_opencv:
        # Convert image to numpy array
        image = convert_to_nparray(image)
        return cv2.resize(image, new_size, interpolation = cv2.INTER_LINEAR)
    else:
        if max(new_size) / max(image.size) >= 0.5:
            method = Image.BILINEAR
        else:
            method = Image.BICUBIC
        image = image.resize(new_size, method)
        return image


def predict_url(imageUrl):
    """
    predicts image by url
    """
    log_msg("Predicting from url: " +imageUrl)
    with urlopen(imageUrl) as testImage:
        image = Image.open(testImage)
        return predict_image(image)


def convert_to_nparray(image):
    """
    converts PIL.Image to numpy array and changes RGB order to BGR
    image: inpout PIL image
    returns image as a numpy array
    """
    # RGB -> BGR
    log_msg("Convert to numpy array")
    image = np.array(image)
    return image[:, :, (2,1,0)]


def update_orientation(image):
    """
    corrects image orientation according to EXIF data
    image: input PIL image
    returns corrected PIL image
    """
    exif_orientation_tag = 0x0112
    if hasattr(image, '_getexif'):
        exif = image._getexif()
        if exif != None and exif_orientation_tag in exif:
            orientation = exif.get(exif_orientation_tag, 1)
            log_msg('Image has EXIF Orientation: ' + str(orientation))
            # orientation is 1 based, shift to zero based and flip/transpose based on 0-based values
            orientation -= 1
            if orientation >= 4:
                image = image.transpose(Image.TRANSPOSE)
            if orientation == 2 or orientation == 3 or orientation == 6 or orientation == 7:
                image = image.transpose(Image.FLIP_TOP_BOTTOM)
            if orientation == 1 or orientation == 2 or orientation == 5 or orientation == 6:
                image = image.transpose(Image.FLIP_LEFT_RIGHT)
    return image


def preprocess_image_opencv(image_pil):
    """
    image_pil: PIL Image, already converted to 'RGB' and correctly oriented
    returns: nparray of extracted crop
    """
    image = convert_to_nparray(image_pil)
    h, w = image.shape[:2]

    min_size = min(h,w)
    crop_size = min(min_size, int(min_size * network_input_size / 256.0))
    startx = max(0, int(max(0, w//2-(crop_size//2))))
    starty = max(0, int(max(0, h//2-(crop_size//2))))
    new_size = (network_input_size, network_input_size)
    log_msg(f"crop: {w}x{h}  to {crop_size}x{crop_size}, origin at {startx}, {starty}, target = {network_input_size}")
    return cv2.resize(image[starty:starty+crop_size, startx:startx+crop_size], new_size, interpolation = cv2.INTER_LINEAR)


def preprocess_image(image_pil):
    """
    image_pil: PIL Image, already converted to 'RGB' and correctly oriented
    returns: nparray of extracted crop
    """
    # If the image has either w or h greater than 1600 we resize it down respecting
    # aspect ratio such that the largest dimention is 1600
    image_pil = resize_down_to_1600_max_dim(image_pil)

    # Convert image to numpy array
    image = convert_to_nparray(image_pil)
    
    # Crop the center square and resize that square down to 256x256
    resized_image = extract_and_resize_to_256_square(image)

    # Crop the center for the specified network_input_Size
    return crop_center(resized_image, network_input_size, network_input_size)


def predict_image(image):
    """
    calls model's image prediction
    image: input PIL image
    returns prediction response as a dictionary. To get predictions, use result['predictions'][i]['tagName'] and result['predictions'][i]['probability']
    """
    log_msg('Predicting image')
    try:
        if image.mode != "RGB":
            log_msg("Converting to RGB")
            image = image.convert("RGB")

        w,h = image.size
        log_msg("Image size: " + str(w) + "x" + str(h))
        
        # Update orientation based on EXIF tags
        image = update_orientation(image)
        
        if use_opencv:
            cropped_image = preprocess_image_opencv(image)
        else:
            cropped_image = preprocess_image(image)

        tf.compat.v1.reset_default_graph()
        tf.import_graph_def(graph_def, name='')

        with tf.compat.v1.Session() as sess:
            prob_tensor = sess.graph.get_tensor_by_name(output_layer)
            predictions, = sess.run(prob_tensor, {input_node: [cropped_image] })
            
            result = []
            for p, label in zip(predictions, labels):
                truncated_probablity = np.float64(round(p,8))
                if truncated_probablity > 1e-8:
                    result.append({
                        'tagName': label,
                        'probability': truncated_probablity,
                        'tagId': '',
                        'boundingBox': None })

            response = { 
                'id': '',
                'project': '',
                'iteration': '',
                'created': datetime.utcnow().isoformat(),
                'predictions': result 
            }

            log_msg("Results: " + str(response))
            return response
            
    except Exception as e:
        log_msg(str(e))
        return 'Error: Could not preprocess image for prediction. ' + str(e)