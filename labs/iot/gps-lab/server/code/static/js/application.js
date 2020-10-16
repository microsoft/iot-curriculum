
var map, datasource, client, popup, searchInput, resultsPanel, searchInputLength, centerMapOnResults;

//The minimum number of characters needed in the search input before a search is performed.
var minSearchInputLength = 3;

//The number of ms between key strokes to wait before performing a search.
var keyStrokeDelay = 150;

function GetMap()
{
    //Initialize a map instance.
    map = new atlas.Map('myMap', {
        center: [-122.64, 47.58],
        zoom: 4,
        view: "Auto",
        style: "satellite",
        authOptions: {
            authType: 'subscriptionKey',
            //subscriptionKey: '<Azure_Map_Subscription_Key>'
            subscriptionKey: 'O_azZVgz2yPHC_nLbTntZzbcpZF7LYx7kO87PfcOv70'
        }
    });

    //Wait until the map resources are ready.
    map.events.add('ready', function ()
    {
        //Add the zoom control to the map.
        map.controls.add(new atlas.control.ZoomControl(), {
            position: 'top-right'
        });
    });
}

$(document).ready(function ()
{
    console.log("Socket Started -- ");

    //connect to the socket server.
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/get_data');

    //receive details from server
    socket.on('mapdata', function (msg)
    {
        console.log("Received data");

        $('#log').html('p>' + msg.data + '</p>');

        var data = JSON.parse(msg.data);

        var dataSource = new atlas.source.DataSource();
        map.sources.add(dataSource);
        console.log([data.longitude, data.latitude]);
        var point = new atlas.Shape(new atlas.data.Point([++data.longitude, ++data.latitude]));

        //Add the symbol to the data source.
        dataSource.add([point]);
        map.layers.add(new atlas.layer.SymbolLayer(dataSource, null));
    });

});