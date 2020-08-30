#include "WebServer.h"

#include <Arduino.h>
#include <esp_camera.h>
#include <SPIFFS.h>

#define FILE_PHOTO "/photo.jpg"

const char index_html[] PROGMEM = R"rawliteral(
<!DOCTYPE HTML>
<html>

<head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {
            text-align: center;
        }

        .vert {
            margin-bottom: 10%;
        }

        .hori {
            margin-bottom: 0%;
        }
    </style>
</head>

<body>
    <div id="container">
        <h2>ESP32-CAM Last Photo</h2>
        <p>It might take more than 5 seconds to capture a photo.</p>
        <p>
            <button id="rotateButton">ROTATE</button>
            <button id="captureButton">CAPTURE PHOTO</button>
        </p>
        <div><img src="saved-photo" id="photo" width="70%"></div>
</body>
<script>
    window.addEventListener("DOMContentLoaded", function () {
        var deg = 0;
        var rotateButton = document.getElementById("rotateButton");
        var captureButton = document.getElementById("captureButton");
        var img = document.getElementById("photo");
        var capturingImageText = document.getElementById("capturingImageText");

        rotateButton.addEventListener('click', function () {
            deg += 90;
            if (isOdd(deg / 90)) { document.getElementById("container").className = "vert"; }
            else { document.getElementById("container").className = "hori"; }
            img.style.transform = "rotate(" + deg + "deg)";
        });

        captureButton.addEventListener('click', function () {
            rotateButton.disabled = true;
            captureButton.disabled = true;

            const getResult = async () => {
                var result = await fetch('capture', {
                    method: 'GET'
                })

                var textResult = await result.text()
                location.reload();
            }
            getResult()
        });

        function isOdd(n) { return Math.abs(n % 2) == 1; }
    });
</script>

</html>)rawliteral";

WebServer::WebServer(uint16_t port) :
    _port(port),
    _webServer(port),
    _camera(),
    _imageHandler()
{
}

// Capture Photo and Save it to SPIFFS
void WebServer::CapturePhotoSaveSpiffs()
{
    camera_fb_t *fb = NULL; // pointer
    bool ok = 0;            // Boolean indicating if the picture has been taken correctly

    do
    {
        // Take a photo with the camera
        Serial.println("Taking a photo...");

        fb = _camera.TakePhoto();
        if (!fb)
        {
            Serial.println("Camera capture failed");
            return;
        }

        Serial.printf("Picture file name: %s\n", FILE_PHOTO);
        ok = _imageHandler.SavePhoto(fb, FILE_PHOTO);

        // Insert the data in the photo file
        if (!ok)
        {
            Serial.println("File write failed");
        }
        else
        {
            Serial.print("The picture has been saved in ");
            Serial.println(FILE_PHOTO);
        }

        _camera.ReleaseFrameBuffer(fb);
    } while (!ok);
}

bool WebServer::Init()
{
    // Camera init
    esp_err_t err = _camera.Init();
    if (err != ESP_OK)
    {
        Serial.printf("Camera init failed with error 0x%x", err);
        ESP.restart();
        return false;
    }

    if (_imageHandler.Init())
    {
        delay(500);
        Serial.println("SPIFFS mounted successfully");
    }
    else
    {
        Serial.println("An Error has occurred while mounting SPIFFS");
        return false;
    }

    // Route for root / web page
    _webServer.on("/", HTTP_GET, [](AsyncWebServerRequest *request) {
        request->send_P(200, "text/html", index_html);
    });

    _webServer.on("/capture", HTTP_GET, [this](AsyncWebServerRequest *request) {
        CapturePhotoSaveSpiffs();
        delay(2000);
        request->send_P(200, "text/plain", "Taking Photo");
    });

    _webServer.on("/saved-photo", HTTP_GET, [](AsyncWebServerRequest *request) {
        request->send(SPIFFS, FILE_PHOTO, "image/jpg", false);
    });

    // Start server
    _webServer.begin();

    return true;
}