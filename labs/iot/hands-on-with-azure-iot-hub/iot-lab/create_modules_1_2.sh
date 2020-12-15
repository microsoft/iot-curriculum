#!/bin/bash

source config.sh

echo ""

#MODULE 1
log "MODULE 1"
log "Creating RG $resourceGroup in $region"
az group create --name $resourceGroup --location $region > /dev/null

log "Deploying IoT Hub"
az iot hub create -g $resourceGroup -n $groupId --sku F1 --partition-count 2 > /dev/null

log "Creating IoT device"	
az iot hub device-identity create --device-id $deviceId --hub-name $groupId > /dev/null

log "MODULE 2"

log "Deploying client VM"
az deployment group create --no-wait --resource-group $resourceGroup --name "client"  --template-file "clientdeploy.json" \
	--parameters environmentName=$clientEnvironment \
	--parameters adminUsername=$vmUser \
	--parameters adminUserPassword=$vmUserPassword \
	--parameters hostnameDNS=$groupId

CLIENT_HOSTNAME=$(az network public-ip list -g $resourceGroup --query "[0].dnsSettings.fqdn" -o tsv)
log "Connect to client in: "
echo "ssh -o 'StrictHostKeyChecking no' $vmUser@$CLIENT_HOSTNAME"

log "Device Connection String"
az iot hub device-identity show-connection-string --device-id $deviceId --hub-name $groupId -o tsv
