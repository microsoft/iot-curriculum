// Copyright (c) Microsoft Corporation.
// Licensed under the MIT license.

#include "ImageHandler.h"

#include <Arduino.h>
#include <SPIFFS.h>

// Initialise the SPIFFS file system
ImageHandler::ImageHandler()
{
    // Initialize the SPIFFS file system
    if (!SPIFFS.begin(true))
    {
        // If the file system initialization fails, restart the board
        ESP.restart();
    }

    delay(500);
    Serial.println("SPIFFS mounted successfully");
}

// Saves the image in the given frame buffer to a file with the given name
bool ImageHandler::SavePhoto(camera_fb_t *frameBuffer, const char *fileName)
{
    bool saved = false;
    int retry = 0;

    // Sometimes the save can fail, so retry up to 10 times
    while (!saved && retry < 10)
    {
        // Check if the file already exists, and if so delete it
        if (SPIFFS.exists(fileName))
        {
            SPIFFS.remove(fileName);
        }

        // Open the file for writing to
        File file = SPIFFS.open(fileName, FILE_WRITE);

        // If the file fails to open, report the error and try again
        if (!file)
        {
            Serial.println("Failed to open file in writing mode");
            saved = false;
            ++retry;
        }
        else
        {
            // Write the framebuffer to the file
            file.write(frameBuffer->buf, frameBuffer->len);

            // Close the file
            file.close();

            // check if file has been correctly saved in SPIFFS
            saved = CheckPhoto(fileName);
        }
    }

    return saved;
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