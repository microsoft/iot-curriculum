#ifndef _WEBSERVER_H_
#define _WEBSERVER_H_

#include "Camera.h"
#include "ImageHandler.h"

#include <ESPAsyncWebServer.h>
#include <string>

using namespace std;

/**
 * @brief A web server that serves up pages to control the camera.
 */
class WebServer
{
public:
    /**
     * @brief Create the web server running on the given port. Initializes webserver and starts serving up pages
     * If the initialization of the web server fails, the board is rebooted.
     *
     * @param port The port to use.
     */
    WebServer(uint16_t port = 50);

private:
    AsyncWebServer _webServer;
    Camera _camera;
    ImageHandler _imageHandler;

    /**
     * @brief Capture a photo from the camera and save it to the SPIFFS file system.
     *
     * @return An error message or error, or OK
     */
    string CapturePhotoAndSaveToSpiffs();
};

#endif