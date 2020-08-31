#ifndef _CAMERA_H_
#define _CAMERA_H_

#include <esp_camera.h>

/**
 * @brief A helper class for interacting with the ESP-EYE camera.
 */
class Camera
{
public:
    /**
     * @brief Initializes the camera class.
     * If the initialization of the camera fails, the board is rebooted.
     */
    Camera();

    /**
     * @brief Takes a photo and returns it as a frame buffer.
     *
     * @return A pointer to an image frame buffer on success, otherwise null
     */
    camera_fb_t *TakePhoto();

    /**
     * @brief Releases the frame buffer after it has been processed.
     * Call this to clean up the memory used by the frame buffer.
     *
     * @param frameBuffer The frame buffer to clean up.
     */
    void ReleaseFrameBuffer(camera_fb_t *frameBuffer);
};

#endif
