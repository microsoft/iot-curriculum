# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for full license information.

cmake_minimum_required(VERSION 3.1)

set (AZUREIOT_SDK_FOLDER "./.build/azure-iot-sdk-c")

set (CMAKE_C_STANDARD 99)
set (CMAKE_CXX_STANDARD 11)

set(AZUREIOT_INC_FOLDER ${AZUREIOT_SDK_FOLDER} 
                        "${AZUREIOT_SDK_FOLDER}/certs"
                        "${AZUREIOT_SDK_FOLDER}/iothub_client"
                        "${AZUREIOT_SDK_FOLDER}/iothub_client/inc")

include_directories(${AZUREIOT_INC_FOLDER} 
                    "${AZUREIOT_SDK_FOLDER}/deps/umock-c/inc"
                    "${AZUREIOT_SDK_FOLDER}/deps/azure-macro-utils-c/inc"
                    "${AZUREIOT_SDK_FOLDER}/c-utility/inc")

link_directories("${AZUREIOT_SDK_FOLDER}/cmake/iothub_client"
                 "${AZUREIOT_SDK_FOLDER}/cmake/umqtt"
                 "${AZUREIOT_SDK_FOLDER}/cmake/c-utility"
                 "${AZUREIOT_SDK_FOLDER}/cmake/deps/uhttp"
                 "${AZUREIOT_SDK_FOLDER}/cmake")

set(app_files
    ../ssh-proxy-client.c
    ${AZUREIOT_SDK_FOLDER}/certs/certs.c
)

add_executable(ssh-proxy-client ${app_files})

target_link_libraries(ssh-proxy-client
    iothub_client_mqtt_transport
    iothub_client
    umqtt
    uhttp
    aziotsharedutil
    parson
    uuid
    pthread
    curl
    ssl
    crypto
    m
)
