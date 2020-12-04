# Run the image classifier on the Raspberry Pi using IoT Edge

In the previous step, you controlled the Pi with either [the keyboard](./iot-hub-control), or [a button and LEDs using a Grove Pi+ kit](./pi-button-led.md).

In this step you will run the image classifier on the Raspberry Pi using IoT Edge.

## IoT Edge

IoT on the Edge involves running workloads that you would traditionally run in the cloud on an IoT device so that it is closer to your data. This has a number of upsides:

* It can be faster, and reduces bandwidth needs as you are not uploading data to the internet - for example if you want to run live video analytics on a video stream you don't need to upload that stream continually over the internet, you can analyze it locally.
* The data stays local - this could be important for privacy considerations, such as medical data
* It can be cheaper - by using your own hardware yo don't have to pay cloud fees

The traditional IoT Edge use case is AI on the edge. You train a model using the power of the cloud, then download the model to run on an Edge device. This is what you will be doing in this lab - taking the model trained by Custom Vision and running in on the Raspberry Pi.

## Set up IoT Edge

[Azure IoT Edge](https://azure.microsoft.com/services/iot-edge/?WT.mc_id=academic-7372-jabenn#create) consists of a run time that runs on your edge device, and a connection to IoT Hub to manage the workloads that need to be deployed to the edge device. Workloads are deployed as containers, from somewhere like the Azure Container Registry.

### Create an IoT Edge device in the IoT Hub

To connect an edge device to IoT Hub, a device needs to be created in IoT Hub, in a similar way as a non-edge IoT device.

1. Open the Azure Portal, and head to the IoT Hub

1. From the side menu, select *Automatic Device Management -> IoT Edge*

    ![The iot edge menu](../images/iot-hub-iot-edge-menu.png)

1. Select the **+ Add an IoT Edge device** button

    ![The add an iot edge device button](../images/iot-hub-iot-edge-add-device-button.png)

1. Set the *Device ID* to `raspberry-pi`

1. Make sure the *Authentication type* is set to  `Symmetric key`, *Auto-generate keys* is checked and *Connect this device to an IoT hub* is set to `Enabled`

1. Select the **Save** button

![The device settings](../images/iot-hub-iot-edge-new-device-settings.png)

### Get the connection string

Once the edge device has been created, the blade will return to the devices list and the new device will be shown.

> If the new device is not shown in the list, select the **Refresh** button

For the IoT Edge agent on the Pi to connect to the IoT Hub as this device, it needs the connection string. This is made up of 3 parts - the URL of the IoT Hub, the device id, and a secret key, the same as for a non-edge IoT device

1. Select the new `raspberry-pi` device in the list

1. Copy the *Primary Connection String* using the **Copy to clipboard** button, and keep a note of this somewhere

### Install the IoT Edge agent

To connect as an edge device, the IoT Edge agent needs to be installed on the Pi.

1. Connect to the Pi from VS Code and launch the terminal

1. Make sure your Pi is up to date by running the following command:

    ```sh
    sudo apt update && sudo apt upgrade --yes && sudo reboot
    ``

    This will update the Pi and reboot it, so reconnect from VS Code after it has finished rebooting

1. Run the following commands to install and register the Microsoft packages list, as well as installing the Microsoft public key:

    ```sh
    curl https://packages.microsoft.com/config/debian/stretch/multiarch/prod.list > ./microsoft-prod.list
    sudo cp ./microsoft-prod.list /etc/apt/sources.list.d/
    curl https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > microsoft.gpg
    sudo cp ./microsoft.gpg /etc/apt/trusted.gpg.d/
    rm ./microsoft-prod.list
    rm ./microsoft.gpg
    ```

1. Run the following command to install the Moby container engine to support the containers needed by the IoT Edge runtime

    ```sh
    sudo apt update
    sudo apt install moby-engine --yes
    ```

1. Run the following command to install the Azure IoT Edge runtime

    ```sh
    sudo apt install iotedge --yes
    ```

### Configure the IoT Edge agent

To connect to your IoT Hub, the IoT Edge agent needs to be configured with the device connection string.

1. Open the `config.yaml` file on the using the `nano` tool in the terminal in VS Code. It needs to be opened as a super user, so can't be edited in VS Code.

    ```sh
    sudo nano /etc/iotedge/config.yaml
    ```

1. Navigate using the arrow keys to the Manual provisioning configuration section:

    ```sh
    # Manual provisioning configuration using a connection string
    provisioning:
      source: "manual"
      device_connection_string: "<ADD DEVICE CONNECTION STRING HERE>"
      dynamic_reprovisioning: false
    ```

1. Delete `<ADD DEVICE CONNECTION STRING HERE>` and paste in your connection string inside the double quotes

1. Save the file and exit nano by using `Ctrl+X`, then press `y` when asked to save the modified buffer, then press `return` to save as the same file

1. Restart the IoT Edge runtime using the following command

    ```sh
    sudo systemctl restart iotedge
    ```

1. You can check the status of the IoT Edge agent with the following command:

    ```sh
    sudo iotedge check
    ```

    You can ignore any *Production readiness* warnings or errors. The important thing is the connectivity checks should all pass.

    ```output
    Connectivity checks
    -------------------
    √ host can connect to and perform TLS handshake with IoT Hub AMQP port - OK
    √ host can connect to and perform TLS handshake with IoT Hub HTTPS / WebSockets port - OK
    √ host can connect to and perform TLS handshake with IoT Hub MQTT port - OK
    √ container on the default network can connect to IoT Hub AMQP port - OK
    √ container on the default network can connect to IoT Hub HTTPS / WebSockets port - OK
    √ container on the default network can connect to IoT Hub MQTT port - OK
    √ container on the IoT Edge module network can connect to IoT Hub AMQP port - OK
    √ container on the IoT Edge module network can connect to IoT Hub HTTPS / WebSockets port - OK
    √ container on the IoT Edge module network can connect to IoT Hub MQTT port - OK
    ```

## Set up the container registry

The custom vision model will be downloaded as a container, and this needs to be hosted in a container registry for the IoT Edge agent to be able to download it. [Azure Container Registry](https://azure.microsoft.com/services/container-registry/?WT.mc_id=academic-7372-jabenn#create) can host containers for use in your IoT Edge applications.

### Create an Azure Container Registry resource

1. From your browser, navigate to [portal.azure.com/#create/Microsoft.ContainerRegistry](https://portal.azure.com/?WT.mc_id=academic-7372-jabenn#create/Microsoft.ContainerRegistry)

1. In the *Basics* tab, enter the required details:

    1. Select your Azure subscription

    1. Select the `assembly-line-qa` resource group that you created earlier for your Custom Vision resource

    1. For the *Registry name*, enter a unique name. This needs to be globally unique as it will form part of the URL for the connection string. This name can only contain letters and numbers, so use something like `assemblylineqayourname` replacing `yourname` with your name.

    1. Select the location closest to you

    1. Set the *SKU* to basic

    ![The basics tab filled out](../images/container-registry-basics.png)

1. Select the **Review + Create** button, then the **Create** button

1. The deployment will begin, and you will be notified once it is complete. Select the **Go to resource** button to open the resource in the portal.

To push containers to this repository, you will need to be able to login via the `docker` command line on the Pi. To do this, you need to turn on an Admin user.

1. From the side menu, select *Settings -> Access Keys*

    ![The access keys menu item](../images/container-registry-access-keys.png)

1. Enable the *Admin user*

    ![The access keys with the admin used enabled](../images/container-registry-access-keys-admin-enabled.png)

1. Take a note of the *Username* and one of the *password* fields. The username should be the same as the registry name.

## Download the model as a container

Custom vision allows models to be exported in a number of formats including CoreML to run on iOS/macOS, Tensorflow and as a container to run inside IoT Edge.

The model that was created is not exportable as is - the configuration needs to be changed.

### Train a compact model

The model that was created used the *General* domain, creating a model that's good for a wide range of images. This can't be exported, it would just be too large. There is a variant of this domain, called *General (Compact)* that create smaller, exportable models.

1. Head to [CustomVision.ai](https://www.customvision.ai/?WT.mc_id=academic-7372-jabenn) in your browser and open your project

1. Select the **Settings** button

    ![The settings button](../../../../images/custom-vision-settings-button.png)

1. Find the *Domain* settings, and select `General (Compact)`

    ![The domain list](../../../../images/custom-vision-settings-domain-general-compact.png)

1. Select the **Save changes** button

1. Once the settings are saved, the model needs to be re-trained to generate the compact, exportable model. Train the model using the **Train** button and the **Quick Training** method.

### Export the model

The container will need to be built on the Raspberry Pi so that is uses the correct architecture. This means you will need to download it on to the Pi. If you are running VS Code locally on the Pi you can do the following steps from the Chromium browser on the Pi, or you can export the model and copy it to your Pi using `scp`.

1. Once the model has finished training, select the **Export** button

    ![The export button](../../../../images/custom-vision-iteration-export-button.png)

1. From the export dialog, select **Dockerfile**

    ![The docker file export option](../../../../images/custom-vision-iteration-export-docker-button.png)

1. From the Docker file export dialog, drop down the *Choose a version* box and select `ARM (Raspberry Pi 3)`

1. Select the **Export** button to prepare the export, then the **Download** button to download the model

1. If you are not running the browser on your Pi, copy the zip file to the `AssemblyLineControl` folder on the Pi. If you are using VS Code Remote SSH you can just drag and drop the file from Windows Explorer/Finder into the VS Code explorer window. If you are not using VS Code Remote SSH then copy the file with a tool like `scp` or [WinSCP](https://winscp.net/eng/index.php).

1. The model is a zip file, so unzip it into a new folder called `classifier` from the VS Code terminal connected to the Pi using the following command:

    ```sh
    mkdir classifier
    unzip *.zip -d classifier/
    rm *.zip
    sudo chmod +rw ./classifier/**
    ```

    This will create a new folder called `classifier`, unzip the zip file into it, remove the zip file, then set permissions so the contents can be read and written to.

1. Open the `Dockerfile` file from inside the `classifier` folder. This contains the instructions for running the container, including what packages need to be installed inside the container. The latest version of Raspberry Pi OS doesn't install a package needed by the container - `libqtgui4`. Edit the first `RUN` line to add this to the end of the line, adding it to the packages to be installed.

    ```sh
    RUN apt update && apt install -y libjpeg62-turbo libopenjp2-7 libtiff5 libatlas-base-dev libqtgui4
    ```

### Build and tag the container image

To use the container inside IoT Edge, it needs to be built, tagged, then uploaded to an Azure Container Registry. To build this container, you will need to install [Docker](https://docs.docker.com/get-docker/).

1. From the VS Code terminal running on the Pi, run the following command to log into the Azure Container Registry from Docker:

    ```sh
    sudo docker login <registry_name>.azurecr.io
    ```

    Replace `<registry_name>` with the name of your registry.

1. When promoted, enter the username and password for the container registry that you captures earlier. The user name should be the same as your registry name.

1. The container needs to be built and tagged ready for upload to the container registry. Use the following command to build and tag the image:

    ```sh
    sudo docker build -t <registry_name>.azurecr.io/classifier:v1 ./classifier/
    ```

    Replace `<registry_name>` with the name of your registry.

    This will take a while to download and build all the components of the image.

1. Finally push the image to the container registry with the following command:

    ```sh
    sudo docker push <registry_name>.azurecr.io/classifier:v1
    ```

    Replace `<registry_name>` with the name of your registry.

1. To verify it was pushed correctly, head to the Container Registry in the Azure Portal, select *Services -> Repositories*. You should see a *classifier* repository in the list. Select this, then select the *v1* version to see details about the container.

## Deploy the model to the edge

The IoT Edge runtime is now ready to have containers deployed to it. Containers are deployed via the IoT Hub from a container registry - a service that stores and manages versions of different containers. The Custom Vision model can be downloaded as a container, uploaded to a container registry and deployed from there to the Pi.

### Create a deployment manifest

### Deploy the container to the edge

## Call the edge model from the ESP-EYE

## Next steps

In this step you ran the image classifier on the Raspberry Pi using IoT Edge.

In the [next step](./upload-iot-hub.md), you will upload the result data to Azure IoT Hub.
