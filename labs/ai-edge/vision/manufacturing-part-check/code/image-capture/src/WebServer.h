#ifndef _WEBSERVER_H_
#define _WEBSERVER_H_

#include "Camera.h"
#include "ImageHandler.h"

#include <ESPAsyncWebServer.h>

class WebServer
{
public:
    WebServer(uint16_t port = 50);
    bool Init();
    uint16_t getPort() { return _port; }

private:
    AsyncWebServer _webServer;
    Camera _camera;
    ImageHandler _imageHandler;
    uint16_t _port;

    void CapturePhotoSaveSpiffs();
};

#endif