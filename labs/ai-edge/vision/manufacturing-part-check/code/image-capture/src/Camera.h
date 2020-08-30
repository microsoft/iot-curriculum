#ifndef _CAMERA_H_
#define _CAMERA_H_

#include <esp_camera.h>

/**
 * @brief A helper class for interacting with the ESP-EYE camera. Call Init before using the other methods on this class.
 */
class Camera
{
public:
    /**
     * @brief Initializes the camera class. Call this method before using the other methods on this class.
     * If the initialization of the camera fails, the board is rebooted.
     *
     * @return ESP_OK on success
     */
    void Init();

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
