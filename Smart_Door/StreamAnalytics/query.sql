SELECT GetMetadataPropertyValue(IoTHub, '[IoTHub].[ConnectionDeviceId]')  as partitionkey
      , GetMetadataPropertyValue(IoTHub, '[IoTHub].[ConnectionDeviceId]') as deviceid
      ,DoorStatus
      , EventEnqueuedUtcTime as time
      ,device_type
INTO
    doorstatus
FROM
IoTHub 
WHERE device_type = 'door_monitor'
