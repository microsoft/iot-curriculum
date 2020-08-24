import logging
import os
import requests
import azure.functions as func

# Get the environment variables
iot_central_api_token = os.environ['IOT_CENTRAL_API_TOKEN']
maps_key = os.environ['MAPS_KEY']

def will_rain():
    # Build the REST URL with the latitude, longitude and maps key
    lat = 47.6451635
    lon = -122.1327916
    url = 'https://atlas.microsoft.com/weather/forecast/daily/json?api-version=1.0&query={},{}&subscription-key={}'
    url = url.format(lat, lon, maps_key)

    # Make the REST request
    result = requests.get(url)

    # Get the category from the JSON
    result_json = result.json()
    summary = result_json['summary']
    category = summary['category']

    # Return if it will rain
    return category == 'rain'

def needs_watering(soil_moisture):
    # Check if it will rain, if so no need to water
    if (will_rain()):
        return False
    else:
        return soil_moisture < 500

def main(req: func.HttpRequest) -> func.HttpResponse:
    # Log the function was called
    logging.info('Python HTTP trigger function processed a request.')

    # Get the JSON from the request
    req_body = req.get_json()

    # Log the JSON
    logging.info(req_body)

    # The JSON can contain a single telemetry record or a list
    # If it's a list, get the last item
    if isinstance(req_body, list):
        req_body = req_body[-1]

    # Get the telemetry values
    temperature = req_body['temperature']
    pressure = req_body['pressure']
    humidity = req_body['humidity']
    soil_moisture = req_body['soil_moisture']

    # Log the values
    logging.info("temperature: %.1f, pressure: %.1f, pressure: %.1f, soil_moisture: %.1f",
                    temperature, pressure, humidity, soil_moisture)

    # Check if the plant needs watering
    request = { 'request' : needs_watering(soil_moisture) }

    # Call the REST API
    url = '<Command REST URL>'
    headers = {'Authorization': iot_central_api_token}

    requests.post(url, headers=headers, json = request)

    # Return a 200 status
    return func.HttpResponse(f"OK")
