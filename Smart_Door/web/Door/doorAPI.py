
from flask import Blueprint, json
from datetime import datetime
from flask import render_template
from Door import app
from flask import Response
from flask import request
import json
import time
from flask import Response, Flask
import random
import sys
from azure.iot.hub import IoTHubRegistryManager

i = 0


db = Blueprint('db', __name__)
#uri =app.config["kafkaurl"]


import azure.cosmos.cosmos_client as cosmos_client
import azure.cosmos.errors as errors
import azure.cosmos.http_constants as http_constants
# Initialize the Cosmos client
endpoint = "https://university-cart.documents.azure.com:443/"
key = 'g4t9RG6mzXscVJMrtkqKPx2R5DEnvr8X7osSBTGmM1j87to1YlOW3BPupwVCPJAi2Lmly2HhMXgTBU71m1cmXA=='

MESSAGE_COUNT = 2
AVG_WIND_SPEED = 10.0
MSG_TXT = "{\"lockunlock\": \"%s\"}"

CONNECTION_STRING = "HostName=University-IoT-Cart.azure-devices.net;SharedAccessKeyName=service;SharedAccessKey=BqDYtCUKJD9QjuoleA8gCRIi/5NjIt797sALbJ2CAU8="
DEVICE_ID = "DoorMonitor001"


# <create_cosmos_client>
#client = cosmos_client.CosmosClient(endpoint, {'masterKey': key})
client = cosmos_client.CosmosClient(endpoint, {'masterKey': key})

database_name = 'cartdemo'

container_name = 'doorstatus'
#database = client.ReadDatabase("dbs/" + database_name)
#database = client.get_database_client(database_name)
#container = database.get_container_client(container_name)
#container = client.ReadContainer("dbs/" + database['id'] + "/colls/" + container_name)
# Enumerate the returned items
import json


@db.route('/status/<string:deviceid>', methods=['GET'])
def dAT(deviceid):
    query = "SELECT top 1 c.DoorStatus FROM c order by c._ts desc"

    dat = []
    for item in  client.QueryItems("dbs/" + database_name + "/colls/" + container_name,
                              query,
                              {'enableCrossPartitionQuery': True}):
        dat.append(item)
    res = json.dumps(dat, indent=True)

    
    
    resp = Response(response=res,
                    status=200,
                    mimetype="application/json")
    return resp






@db.route('/lockunlock/<string:action>', methods=['GET'])
def LockUnlock(action):

    registry_manager = IoTHubRegistryManager(CONNECTION_STRING)

    data = MSG_TXT % action

    props={}
            # optional: assign system properties
#    i = i + 1
#    props.update(messageId = "message_%d" % i)
    #props.update(correlationId = "correlation_%d" % i)
    props.update(contentType = "application/json")

            # optional: assign application properties
    #prop_text = "PropMsg_%d" % i
    #props.update(testProperty = prop_text)

    registry_manager.send_c2d_message(DEVICE_ID, data, properties=props)
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 
