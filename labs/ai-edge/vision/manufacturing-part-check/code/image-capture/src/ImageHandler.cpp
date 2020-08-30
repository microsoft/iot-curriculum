#include "ImageHandler.h"

#include <Arduino.h>
#include <SPIFFS.h>

// Initialise the SPIFFS file system
void ImageHandler::Init()
{
    // Initialize the SPIFFS file system
    if (!SPIFFS.begin(true))
    {
        // If the file system initialization fails, restart the board
        ESP.restart();
    }
}

// Saves the image in the given frame buffer to a file with the given name
bool ImageHandler::SavePhoto(camera_fb_t *frameBuffer, const char *fileName)
{
    // Check if the file already exists, and if so delete it
    if (SPIFFS.exists(fileName))
    {
        SPIFFS.remove(fileName);
    }

    // Open the file for writing to
    File file = SPIFFS.open(fileName, FILE_WRITE);

    // If the file fails to open, report the error and return false
    if (!file)
    {
        Serial.println("Failed to open file in writing mode");
        return false;
    }

    // Write the framebuffer to the file
    file.write(frameBuffer->buf, frameBuffer->len);

    // Close the file
    file.close();

    // check if file has been correctly saved in SPIFFS
    return CheckPhoto(fileName);
}

// Checks if the photo has been saved by validating the file size
bool ImageHandler::CheckPhoto(const char *fileName)
{
    // Open the file from teh SPIFFS file system
    File f_pic = SPIFFS.open(fileName);

    // Get the file size
    unsigned int pic_sz = f_pic.size();

    // JPEG file sizes vary, so check at least 100 bytes were written
    return (pic_sz > 100);
}