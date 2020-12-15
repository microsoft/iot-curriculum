#!/bin/bash 

region="westeurope"
environmentName="icai-iot-lab"

#Resource Groups
resourceGroup=$environmentName

#Read Group Number
read -p " Please enter your group number, (Example == 02h):  " groupNumber

groupNumber=$(python3 group-checker.py $groupNumber)

if [ $? -ne 0 ]
then 
	echo 'ERROR: Your group number must use double digits and c if you are at class and h if you are at home, example 01c'
	exit
fi

#Read user 
read -p " Please enter your VM user: " vmUser

#Read user password
echo "  Password must have 12 characters, a capital letter, small letters, numbers and special characters"
read -p " Please enter your VM user password: " vmUserPassword
python3 password-checker.py $vmUserPassword

if [ $? -ne 0 ]
then
	exit
fi


startTime=$(date +%s )

clientEnvironment=$environmentName"-client"

#groupId
groupId="icaiiotlabgroup"$groupNumber

#IoT Hub
messageStorageContainerName="messagedata"
messageIoTHubRoutingEndpoint="messageStorageEndpoint"
messageIoTHubRouteName="messageStorageRoute"

#IoT device
deviceId="sensor"

function log {
	secondsNow=$(date +%s )
	elapsed=$(expr $secondsNow - $startTime)
	echo "LOGGING - $elapsed s. - "$1
}

az extension add --name azure-iot > /dev/null
