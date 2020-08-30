#include "WebServer.h"

#include <Arduino.h>
#include <esp_camera.h>
#include <SPIFFS.h>
#include <WiFi.h>

// Save the photo to photo.jpg
#define FILE_PHOTO "/photo.jpg"

// The index.html file as a raw string.
// This web page has two buttons:
// Rotate - rotates the image on screen
// Capture photo - captures the photo from the camera and reload the page
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
        <h2>ESP32-EYE Photo Capture</h2>
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

// Create the web server on the given port
WebServer::WebServer(uint16_t port) : _webServer(port),
                                      _camera(),
                                      _imageHandler()
{
    Serial.println("Starting web server...");

    // Route for root / web page
    _webServer.on("/", HTTP_GET, [](AsyncWebServerRequest *request) {
        Serial.println("GET request for /");
        // Return the index_html string as the web page
        request->send_P(200, "text/html", index_html);
    });

    // Route for the /capture end point
    _webServer.on("/capture", HTTP_GET, [this](AsyncWebServerRequest *request) {
        Serial.println("GET request for /capture");
        // Capture and save the photo
        CapturePhotoAndSaveToSpiffs();
        delay(2000);
        request->send_P(200, "text/plain", "Taking Photo");
    });

    // Route for the saved-photo end point
    _webServer.on("/saved-photo", HTTP_GET, [](AsyncWebServerRequest *request) {
        Serial.println("GET request for /saved-photo");
        // Return the file loaded from the SPIFFS file system
        request->send(SPIFFS, FILE_PHOTO, "image/jpg", false);
    });

    // Start the server
    _webServer.begin();

    // Print the Local IP Address once we are connected
    // This is the address you will use to connect to the web server to
    // capture photos
    Serial.println("Web server started:");
    Serial.print("IP Address: http://");
    Serial.print(WiFi.localIP());
    Serial.printf(":%d\r\n", port);
}

// Capture Photo and Save it to SPIFFS
void WebServer::CapturePhotoAndSaveToSpiffs()
{
    camera_fb_t *fb = NULL;
    bool ok = false;

    // Loop whilst the photo capture and save fails
    do
    {
        // Take a photo with the camera
        Serial.println("Taking a photo...");

        fb = _camera.TakePhoto();

        // Verify the photo was taken
        if (!fb)
        {
            Serial.println("Camera capture failed");
            return;
        }

        Serial.printf("Picture file name: %s\n", FILE_PHOTO);

        // Save the photo to the SPIFFS file system
        ok = _imageHandler.SavePhoto(fb, FILE_PHOTO);

        if (!ok)
        {
            Serial.println("File write failed");
        }
        else
        {
            Serial.print("The picture has been saved in ");
            Serial.println(FILE_PHOTO);
        }

        // Release the photo frame buffer
        _camera.ReleaseFrameBuffer(fb);
    } while (!ok);
}
