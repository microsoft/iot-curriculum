# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import os
from azure.cognitiveservices.vision import computervision
from msrest import authentication
from dotenv import load_dotenv

# Load the API key and endpoint from the .env file
load_dotenv()
API_KEY = os.getenv('API_KEY')
ENDPOINT = os.getenv('ENDPOINT')

# Captures an image from a USB web cam and saves it as filename
# This code assumes you only have one web cam attached
def capture_image_from_usb(filename):
    # Import OpenCV
    import cv2

    # Get the first camera
    cam = cv2.VideoCapture(0)

    # Capture a still image
    _, frame = cam.read()

    # Write the image to a file
    cv2.imwrite(filename, frame)

    # Release the camera
    cam.release()    

# Captures an image from a Raspberry Pi camera and saves it as filename
def capture_image_from_picamera(filename):
    # Import the picamera library and the time libraty
    import time
    import picamera

    # Create a camera object to access the camera
    with picamera.PiCamera() as camera:
        # Camera warm-up time
        time.sleep(2)

        # Capture an image from the camera to a file
        camera.capture(filename)

# The filename to save the image to
# Images are saved instead of just being analysed for text directly
# to help with debugging - check the image.png file saved in the current
# folder to debug what the camera is actually seeing. This is great to
# help with things like making sure the camera is the right way up.
filename = 'image.png'

# Uncomment the function calls depending on what camera you are using
# capture_image_from_usb(filename)
# capture_image_from_picamera(filename)

# Create the computer vision client using the API key and endpoint
credentials = authentication.CognitiveServicesCredentials(API_KEY)
computervision_client = computervision.ComputerVisionClient(ENDPOINT, credentials)

# Open the image file for reading
with open(filename, "rb") as image:
    # Look for printed text in the image
    result = computervision_client.recognize_printed_text_in_stream(image)

    # The results come back in regions - defined areas in the image containing
    # text on one or more lines, with one or more words per line
    # To make it easier to see the results, this code flattens all the words
    # in all the lines in all the regions into one array of words
    text_words = []
    for region in result.regions:
        for line in region.lines:
            for word in line.words:
                text_words.append(word.text)
    
    # Show the detected words on the console
    print(text_words)
