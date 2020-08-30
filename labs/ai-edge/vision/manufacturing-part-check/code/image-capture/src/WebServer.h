#ifndef _WEBSERVER_H_
#define _WEBSERVER_H_

#include "Camera.h"
#include "ImageHandler.h"

#include <ESPAsyncWebServer.h>

/**
 * @brief A web server that serves up pages to control the camera.
 */
class WebServer
{
public:
    /**
     * @brief Create the web server running on the given port
     *
     * @param port The port to use.
     */
    WebServer(uint16_t port = 50);
    
    /**
     * @brief Initializes webserver and starts serving up pages. Call this method before using the other methods on this class.
     * If the initialization of the web server fails, the board is rebooted.
     */
    void Init();

private:
    AsyncWebServer _webServer;
    Camera _camera;
    ImageHandler _imageHandler;
    uint16_t _port;

    /**
     * @brief Capture a photo from the camera, and save it to the SPIFFS file system.
     */
    void CapturePhotoAndSaveToSpiffs();
};

#endif