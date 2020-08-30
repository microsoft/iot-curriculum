#include "ImageHandler.h"

#include <Arduino.h>
#include <SPIFFS.h>

bool ImageHandler::Init()
{
    bool retVal = SPIFFS.begin(true);
    if (!retVal)
    {
        ESP.restart();
    }    

    return retVal;
}

bool ImageHandler::SavePhoto(camera_fb_t *frameBuffer, const char *fileName)
{
    if (SPIFFS.exists(fileName))
    {
        SPIFFS.remove(fileName);
    }

    File file = SPIFFS.open(fileName, FILE_WRITE);

    if (!file)
    {
        Serial.println("Failed to open file in writing mode");
        return false;
    }

    file.write(frameBuffer->buf, frameBuffer->len); // payload (image), payload length

    // Close the file
    file.close();

    // check if file has been correctly saved in SPIFFS
    return CheckPhoto(fileName);
}

bool ImageHandler::CheckPhoto(const char *fileName)
{
    File f_pic = SPIFFS.open(fileName);
    unsigned int pic_sz = f_pic.size();
    return (pic_sz > 100);
}