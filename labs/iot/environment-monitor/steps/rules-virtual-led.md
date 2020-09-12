# Set up the virtual IoT device Pi to report to the console triggered by an IoT Central command

In the [previous step](./rules.md) you performed simple analytics and created an alert on the data using IoT Central rules.

In this step you will set up the virtual IoT device to listen for an IoT Central command, and when the command is received send a message to the console.

## IoT Central commands

IoT Central commands are instructions sent by IoT Central to command a device to do something. For example, if a sound level is reaching dangerous levels, IoT Central can send a command to a device.

The command will be set up and tested in a later step - it can't be tested until a device is able to listen for it. In this step, the virtual IoT device will be configured to listen for the command, and when received send a message to the console.

The command will be called `TooLoud`.

## Program the virtual IoT device

The virtual IoT device needs some code changes to listen for the command, and be able to output to the console.

### Update the code to handle the Too Loud command

In this section you will be adding code to the Python file. If you haven't used Python before, be aware it is very specific about how the lines are indented, so make sure the code is indented the same as the code around it. You can find the full code in the [app.py](../code/virtual-device/led/app.py) file in the [code/virtual-device/led](../code/virtual-device/led) folder to check your code against if you get errors.

1. Open the `EnvironmentMonitor` folder in VS Code if it's not already open. Open the `app.py` file.

1. After the `import` statements, add another to import `MethodResponse` from the `azure.iot.device` Pip package, below the line importing from `azure.iot.device.aio`:

    ```python
    from azure.iot.device import MethodResponse
    ```

1. Head to just before the `main_loop`

1. Add the following code before the `main_loop`:

    ```python
    # Asynchronously wait for commands from IoT Central
    # If the TooLoud command is called, handle it and output to the console
    async def command_listener(device_client):
        # Loop forever waiting for commands
        while True:
            # Wait for commands from IoT Central
            method_request = await device_client.receive_method_request("TooLoud")

            # Log that the command was received
            print()
            print("#########################")
            print("Too Loud Command received")
            print("#########################")
            print()

            # IoT Central expects a response from a command, saying if the call
            # was successful or not, so send a success response
            payload = {"result": True}

            # Build the response
            method_response = MethodResponse.create_from_method_request(
                method_request, 200, payload
            )

            # Send the response to IoT Central
            await device_client.send_method_response(method_response)
    ```

    This code sets up a listener for the commands from IoT Central, and if the `TooLoud` command is received, it sends a message to the console, and sends a response to IoT Central to say the command was handled.

1. Head to after the `main_loop` function, after the keyboard listener is declared and before the `await main_loop()` call

1. Add the following code to start the command listener

    ```python
    # Start the command listener
    command_listeners = asyncio.gather(command_listener(device_client))
    ```

1. After the call to `await main_loop`, add the following code:

    ```python
    # Cancel listening
    command_listeners.cancel()
    ```

1. Save the file

1. Run the code from the VS Code terminal using the following command:

    ```sh
    python app.py
    ```

    Leave the code running whilst you do the next step.

## Next steps

In this step you set up the virtual IoT device to listen for an IoT Central command, and when the command was received send a message to the console.

In the [next step](./rules-command.md) you will create the IoT Central command and trigger it from a rule.
