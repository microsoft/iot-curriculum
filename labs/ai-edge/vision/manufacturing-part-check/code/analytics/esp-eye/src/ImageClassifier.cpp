// Copyright (c) Microsoft Corporation.
// Licensed under the MIT license.

#include "ImageClassifier.h"
#include "Config.h"

#include <Arduino.h>
#include <ArduinoJson.h>
#include <esp_http_client.h>

// A string for tracking the response from the web request.
// The ESP web request framework needs a static callback function,
// so rather than returning data, the callback writes to this static string
static string httpResponseString;

// This is a callback function used by the ESP http code to handle HTTP events.
static esp_err_t HttpEventHandler(esp_http_client_event_t *evt)
{
    // For HTTP_EVENT_ON_DATA - the event fired when the HTTP request returns data,
    // save the data returned to the statid response string variable
    if (evt->event_id == HTTP_EVENT_ON_DATA)
    {
        httpResponseString.append((char *)evt->data, evt->data_len);
    }

    // Return OK
    return ESP_OK;
}

// Classify the image using the Custom Vision project specified in the config.h header file,
// and return the most probable tag
string ImageClassifier::ClassifyImage(camera_fb_t *frameBuffer)
{
    // Reset the static respons
    httpResponseString.clear();

    // Create the HTTP client config connecting to the prediction endpoint
    esp_http_client_config_t config = {};
    config.url = predictionUrl;
    config.is_async = false;
    config.event_handler = HttpEventHandler;
    config.timeout_ms = 30000;

    esp_http_client_handle_t client = esp_http_client_init(&config);

    // Set the headers including the Custom Vision prediction key
    esp_http_client_set_method(client, HTTP_METHOD_POST);
    esp_http_client_set_header(client, "Content-Type", "application/octet-stream");
    esp_http_client_set_header(client, "Prediction-Key", predictionKey);

    //Post the image to Azure Custom Vision
    esp_http_client_set_post_field(client, (char *)frameBuffer->buf, frameBuffer->len);

    // Make the web request, and wait for data
    // The web request is asynchronous, so there may be a delay before getting results,
    // so loop checking for the results
    esp_err_t err = ESP_OK;

    do
    {
        err = esp_http_client_perform(client);
        delay(1);
    } while (err == ESP_ERR_HTTP_EAGAIN);

    // Ensure the HTTP call didn't return an error
    if (err != ESP_OK)
    {
        Serial.printf("Error perform http request %s\r\n", esp_err_to_name(err));
        return "Error classifying image";
    }

    // Check for content in the result of the call
    int content_length = esp_http_client_get_content_length(client);
    if (content_length < 0)
    {
        Serial.println("Content-Length is not found");
        return "Error classifying image";
    }

    // Log the status and content to the serial port
    Serial.printf("HTTPS Status = %d, content_length = %d\r\n", esp_http_client_get_status_code(client), content_length);
    Serial.printf("Response: %s\r\n", httpResponseString.c_str());

    // The result is JSON, so decord it
    StaticJsonDocument<2048> resultsDocument;
    deserializeJson(resultsDocument, httpResponseString.c_str());

    // The JSON document has a child array called predictions, containing tags and probability
    // These are in tag order, so loop through them to get the tag with the highest probability
    string topTag = "";
    double topTagProbability = 0;
    
    for (int i = 0; i < resultsDocument["predictions"].size(); ++i)
    {
        double probability = resultsDocument["predictions"][i]["probability"];
        if (probability > topTagProbability)
        {
            topTagProbability = probability;
            topTag = string((const char *)resultsDocument["predictions"][i]["tagName"]);
        }
    }

    Serial.printf("Top prediction = %s\r\n", topTag.c_str());

    // Clean up the HTTP client
    esp_http_client_cleanup(client);

    // Return the most probable tag
    return topTag;
}