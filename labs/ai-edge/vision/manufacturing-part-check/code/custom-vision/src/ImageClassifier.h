#ifndef _IMAGECLASSIFIER_H_
#define _IMAGECLASSIFIER_H_

#include <esp_camera.h>
#include <string>

using namespace std;

/**
 * @brief A helper class for classifying images using the Azure Custom Vision service.
 * https://CustomVision.ai
 */
class ImageClassifier
{
public:
    /**
     * @brief Classify the image using the Custom Vision project defined in config.h.
     *
     * @param frameBuffer The image to classify.
     * @return The most probably tag for the image
     */
    string ClassifyImage(camera_fb_t *frameBuffer);
};

#endif