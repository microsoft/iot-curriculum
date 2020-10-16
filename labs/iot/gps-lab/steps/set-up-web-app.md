# Run the Web Appliction

In this step you will run the web application.

## Steps

1. Open the server solution in Visual Studio or Visual Studio code
2. Install Flask and SocketIO

    ```sh
    pip install Flask
    ```

     ```sh
    pip install Flask-SocketIO
    ```
3. Set up application.py as startup page
4. Please note that you have changed the connection string and consumer groups as specified in the previous steps. [Set up IoT Hub](./set-up-iot-hub.md)
5. Note that you have changed the Azure Maps subscription key as specified in the previous steps. [Set up Azure Maps](./set-up-azure-maps.md)

## Run the Python Code
1. Run the web application
2. Make sure that your Raspberry Pi and GPS sensor is connected and sending data
3. You should see a Azure Maps and a Pin specifying your GPS location.
![Azure Maps](../images/map-view.png)
