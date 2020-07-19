from azure.cognitiveservices.vision import computervision
from msrest import authentication

class Client(object):
    def __init__(self, subscription_key, endpoint):
        credentials = authentication.CognitiveServicesCredentials(subscription_key)
        self.computervision_client = computervision.ComputerVisionClient(endpoint, credentials)
    def get_text_recognition_result_for_image(self, image_path):
        """Returns a text recognition (OCR) result from the computer vision service."""
        with open(image_path, "rb") as image:
            result = self.computervision_client.recognize_printed_text_in_stream(image)
        return result

def join_all_text_from_text_recognition(result):
    """Returns a single string formed by joining each word in the text recognition result by a single space."""
    text_words = []
    for region in result.regions:
        for line in region.lines:
            for word in line.words:
                text_words.append(word.text)
    text = " ".join(text_words)
    return text

