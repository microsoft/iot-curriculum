import os, sys, argparse

from PIL import Image

grandparent_dirpath = os.path.split(os.path.split(os.path.dirname(__file__))[0])[0]
sys.path.append(grandparent_dirpath)

from ocr import capture, sql, vision

parser = argparse.ArgumentParser()
parser.add_argument("--image_path", default=os.path.join(grandparent_dirpath, 'captured.png'))
parser.add_argument("--subscription_key", required=True)
parser.add_argument("--endpoint", required=True)
parser.add_argument("--connection_string", required=True)
parsed_args = parser.parse_args()

# Capture and save the image as a PNG file as required by the computer vision service.

image = capture.get_image_from_camera()

image_as_array = Image.fromarray(image, 'RGB')
image_as_array.save(parsed_args.image_path)

# Get the text recognition (ORC) result from the computer vision service and
# transform it into a single text string that is inserted into the SQL DB

vision_client = vision.Client(parsed_args.subscription_key, parsed_args.endpoint)
result = vision_client.get_text_recognition_result_for_image(parsed_args.image_path)

text = vision.join_all_text_from_text_recognition(result)

text_db = sql.Text(parsed_args.connection_string)
text_db.insert_text(sql.Text.VISION, text)