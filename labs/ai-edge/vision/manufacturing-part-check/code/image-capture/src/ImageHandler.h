#ifndef _IMAGEHANDLER_H_
#define _IMAGEHANDLER_H_

#include "esp_camera.h"

/**
 * @brief A helper class for saving photos. Call Init before using the other methods on this class.
 */
class ImageHandler
{
public:
    /**
     * @brief Initializes the image handler class. Call this method before using the other methods on this class.
     * If the initialization of the file system fails, the board is rebooted.
     */
    void Init();

    /**
     * @brief Saves the given frame buffer to a file with the given name.
     *
     * @param frameBuffer The frame buffer to save.
     * @param fileName The file name to save to.
     * 
     * @return TRUE on success
     */
    bool SavePhoto(camera_fb_t *frameBuffer, const char *fileName);

private:

    /**
     * @brief Checks the image saved correctly by validating bytes were written.
     *
     * @param fileName The file name to check.
     * 
     * @return TRUE on if the file was saved correctly, otherwise FALSE
     */
    bool CheckPhoto(const char *fileName);
};

#endif