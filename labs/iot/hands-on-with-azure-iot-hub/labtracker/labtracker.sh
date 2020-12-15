#!/bin/bash

firstGroup=14
numGroups=16

groupNamePrefix="icaiiotlabgroup"
region="westeurope"
resultFile="/home/sergio/index.html"

group_exclusions=('14h' '15h')

group_letters=('c' 'h')

cat <<EOF > $resultFile
<!DOCTYPE html>
<html>
<head>
	<title>Lab validator</title>
	<meta http-equiv="refresh" content="10">
	<meta charset="UTF-8">
	<style>
		table, th, td {
		border: 1px solid black;
		text-align: center;
		}
	</style>

</head>
<body>

<table id="test"><tr><th>GroupID</th><th>Azure IoT Hub</th><th>Device VM</th><th>Storage Account IoT</th><th>Storage Account TSI</th></tr>
EOF


function checkDomain {
	domain=$1

	response=$(nslookup $domain | egrep -o "canonical|NXDOMAIN")

	if [ $response"a" = "canonicala" ]
	then
		echo "OK"
	elif [ $response"a" = "a" ]
	then
		echo "OK"
	else
		echo "KO"
	fi 
	
}	
#Check IoT Hub
function checkIoTHub {
	groupId=$1
	thisGroup=$groupNamePrefix$groupId
	domain=$thisGroup".azure-devices.net"
	checkDomain $domain
	
}

#Check Storage Account for IoT
function checkStorageAccountIoT {
	groupId=$1
	thisGroup=$groupNamePrefix$groupId
	domain=$thisGroup".blob.core.windows.net"
	checkDomain $domain
	
}

#Check Storage Account for TSI
function checkStorageAccountTSI {
	groupId=$1
	thisGroup=$groupNamePrefix$groupId"tsi"
	domain=$thisGroup".blob.core.windows.net"
	checkDomain $domain
	
}

#Check VM
function checkDeviceVM {
	groupId=$1
	thisGroup=$groupNamePrefix$groupId
	domain=$thisGroup".$region.cloudapp.azure.com"
	checkDomain $domain
	
}

containsElement () {
  local e match="$1"
  shift
  for e; do [[ "$e" == "$match" ]] && return 0; done
  return 1
}

for groupNumber in $(seq $firstGroup $numGroups)
do
	#Check letters
	for group_letter in ${group_letters[@]}
	do
		
		groupId=$groupNumber$group_letter 
		containsElement  $groupId "${group_exclusions[@]}"
	
		if [ $? -eq 0 ]
		then
			continue
		fi

		iotHub=$(checkIoTHub               $groupId)
		storAcIoT=$(checkStorageAccountIoT $groupId)
		deviVM=$(checkDeviceVM             $groupId)
		storAcTSI=$(checkStorageAccountTSI $groupId)
		
		echo "<tr><td>$groupId</td><td>$iotHub</td><td>$storAcIoT</td><td>$deviVM</td><td>$storAcTSI</td></tr>" >> $resultFile
	done
done

echo "</table>" >> $resultFile
echo 	"
<script>
	var cells = document.getElementsByTagName('td');
	for (var i = 0; i < cells.length; i++) {
		if (cells[i].innerHTML == 'KO') {
			cells[i].style.backgroundColor = 'red';
		}
		if (cells[i].innerHTML == 'OK') {
			cells[i].style.backgroundColor = 'green';
		}
	}
</script>" >> $resultFile


echo "</body></html>" >> $resultFile