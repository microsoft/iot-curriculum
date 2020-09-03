// Copyright (c) Microsoft Corporation.
// Licensed under the MIT license.

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
        <h2>ESP32-EYE Image Classifier</h2>
        <p>
            <button id="takePictureButton">Take photo</button>
        </p>
        <p id="resultText"></p>
        <div><img src="saved-photo" id="photo" width="70%"></div>
</body>
<script>
    window.addEventListener("DOMContentLoaded", function () {
        var takePictureButton = document.getElementById("takePictureButton");
        var img = document.getElementById("photo");
        var resultText = document.getElementById("resultText");

        takePictureButton.addEventListener('click', function () {
            takePictureButton.disabled = true;

            const getResult = async () => {
                var result = await fetch('capture', {
                    method: 'GET'
                })

                resultText.textContent = await result.text()
                img.src = "saved-photo#" + new Date().getTime();

                takePictureButton.disabled = false;
            }
            getResult()
        });
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
        string result = CapturePhotoAndSaveToSpiffs();
        request->send_P(200, "text/plain", result.c_str());
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
string WebServer::CapturePhotoAndSaveToSpiffs()
{
    // Take a photo with the camera
    Serial.println("Taking a photo...");
    camera_fb_t *fb = _camera.TakePhoto();

    // Verify the photo was taken
    if (!fb)
    {
        Serial.println("Camera capture failed");
        return "Error capturing from camera";
    }

    Serial.printf("Picture file name: %s\n", FILE_PHOTO);

    // Classify the photo
    string result = "OK";

    // Save the photo to the SPIFFS file system
    if (!_imageHandler.SavePhoto(fb, FILE_PHOTO))
    {
        Serial.println("File write failed");
        result = "Error saving file";
    }

    _camera.ReleaseFrameBuffer(fb);

    return result;
}
