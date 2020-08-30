#ifndef _IMAGEHANDLER_H_
#define _IMAGEHANDLER_H_

#include "esp_camera.h"

class ImageHandler
{
public:
    bool Init();
    bool SavePhoto(camera_fb_t *frameBuffer, const char *fileName);

private:
    bool CheckPhoto(const char *fileName);
};

#endif