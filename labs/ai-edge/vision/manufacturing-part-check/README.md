# Manufacturing part checker

This lab shows how to build a prototype part checker using AI to validate that parts are manufactured correctly.

# Pi Configuration

```sh
# Update all the things
sudo apt update && sudo apt upgrade -y
sudo reboot

# Install the Grove stuff
sudo curl -kL dexterindustries.com/update_grovepi | bash
sudo reboot

# Update the Grove firmware
git clone https://github.com/DexterInd/GrovePi.git
cd GrovePi/Firmware
sudo ./firmware_update.sh

# Install docker
curl -sSL https://get.docker.com | sh
sudo usermod -aG docker pi
sudo reboot

# Install IoT Edge
curl https://packages.microsoft.com/config/debian/stretch/multiarch/prod.list > ./microsoft-prod.list
sudo cp ./microsoft-prod.list /etc/apt/sources.list.d/
curl https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > microsoft.gpg
sudo cp ./microsoft.gpg /etc/apt/trusted.gpg.d/
sudo apt update
sudo apt -y install iotedge

sudo nano /etc/iotedge/config.yaml
# Set connection string
sudo systemctl restart iotedge

# Install IoT Hub python packages
sudo apt install cmake libssl-dev -y
pip3 install azure-iot-hub
pip3 install python-dotenv

```