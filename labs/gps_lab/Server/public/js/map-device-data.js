/* eslint-disable max-classes-per-file */
/* eslint-disable no-restricted-globals */
/* eslint-disable no-undef */
$(document).ready(() => {
  // if deployed to a site supporting SSL, use wss://
  const protocol = document.location.protocol.startsWith('https') ? 'wss://' : 'ws://';
  const webSocket = new WebSocket(protocol + location.host);

  // When a web socket message arrives:
  // 1. Unpack it
  // 2. Add the symbol layer in the map
  webSocket.onmessage = function onMessage(message) {
    console.log(message);
   var data = JSON.parse(message.data).IotData; 

    var dataSource = new atlas.source.DataSource();
    map.sources.add(dataSource);
    console.log([data.longitude, data.latitude]);
    var point = new atlas.Shape(new atlas.data.Point([ ++data.longitude, ++data.latitude]));
    //Add the symbol to the data source.
    dataSource.add([point]);
    map.layers.add(new atlas.layer.SymbolLayer(dataSource, null));
  };
});
