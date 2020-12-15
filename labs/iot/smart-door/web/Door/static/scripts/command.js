


$(function () {

    $.get("command/All", function (data) {

        var obj = $('#command');

        $.each(data, function (index, value) {
            var a = $('<a href="#" class="list-group-item" data-command="' + value + '" onclick="CommandDetail(this)">' + value + '</a>')
            obj.append(a)
        });
    });
});

function CommandDetail(a) {
    that = $(a)
   
    var obj = $('#command');
    obj.hide();
    cmdMess = $('#commandMessages');
    cmdMess.show();

    $.get("commands/" + that.data('command'), function (data)
    {

        var obj = $('#command');
        $.each(data, function (index, value)
        {
            var id = value._id.$oid;
            html = '<a href="#" class="list-group-item" data-order="' + value.Order + '" data-command="' + that.data('command') + '" onclick="EditDetail(this)">' + value.Action +  (value.FriendlyName || '') 
//            html = '<a href="#" class="list-group-item" data-order="' + value.Order + '" data-command="' + that.data('command') + '" onclick="EditDetail(this)">' + value.Action + ' <span class="menuItem">' + (value.FriendlyName || '') + '</span>'

            switch (value.Action)
            {
                case 'Gripper':
                    html += '<div class="subitem" id="">' + value.Open + '</div>'
                    break;
                case 'Move':
                    
                    html += MakeMove(value,id)

                    break;
                default:
                    colsole.log('"' + value.Action+ "'")
            }



            html += '</a>'
            cmdMess.append($(html))


        });



    });
}

function MakeMove(value, id) {
   var html = '';
    try {
        html += '<div  class="subitem">'
        html += '<div  class="col1" id="post'+value.Order+'">'
        html += '<h5>Cartisian</h5>'
        html += '<h6>Robot</h6>'
        html += '<input type="hidden" id="Name'+ id+ '" value="'+value.Name+'">'
        html += EditCar(value.Cartisian.position.x, 'position', 'x', id)
        html += EditCar(value.Cartisian.position.y, 'position', 'y', id)
        html += EditCar(value.Cartisian.position.z, 'position', 'z', id)
        html += '<h6>Hand</h6>'
        html += EditCar(value.Cartisian.orientation.x, 'orientation', 'x', id)
        html += EditCar(value.Cartisian.orientation.y, 'orientation', 'y', id)
        html += EditCar(value.Cartisian.orientation.z, 'orientation', 'z', id)
        html += EditCar(value.Cartisian.orientation.w, 'orientation', 'w', id)
        html += '</div>'

        html += '<div  class="col2">'
        html += GroupInfo(value)
        html += '</div>'
        html += '<div  class="col3">'
        html += GroupButtons(value)
        html += '</div>'
        html += '</div>'
        //  console.log(html)
    } catch (ex) { alert(ex) }
    return html;

}

function GroupInfo(value)
{


    var template = $('#CommandInfo').html();
    var html = Mustache.to_html(template, value);
    return html;
}

function getValues(id)
{
    var Command = {}

    Command.Cartisian = {}

    Command.Cartisian.position = {}
    Command.Cartisian.orientation = {}
    Command.Cartisian.position.x = $('#positionx' + id).val()
    Command.Cartisian.position.y = $('#positiony' + id).val()
    Command.Cartisian.position.z = $('#positionz' + id).val()
    Command.Cartisian.orientation.w = $('#orientationw' + id).val()
    Command.Cartisian.orientation.x = $('#orientationx' + id).val()
    Command.Cartisian.orientation.y = $('#orientationy' + id).val()
    Command.Cartisian.orientation.z = $('#orientationz' + id).val()
    Command._id = id;
    Command.FriendlyName = $('#FriendlyName' + id).val()
    Command.Action = $('#Action' + id).val()
    Command.Order = $('#Order' + id).val()
    Command.Speed= $('#Speed' + id).val()
    Command.Name = $('#Name' + id).val()
    return Command;
}

function MoveNow(that, id)
{
    var Command = getValues(id);
    $.post("/robot/Move",
        Command,
        function (data, status) {
           // alert("Data: " + data + "\nStatus: " + status);
        });

}

function DeleteRecord(that, id) {

//    var Command = getValues(id);

    Id = {}
    Id.id = id;

    $.post("/command/Delete",
        Id,
        function (data, status) {
            //alert("Data: " + data + "\nStatus: " + status);
        });



}




function SaveDetails(that, id)
{

    var Command = getValues(id);
    
   
    
    $.post("/command/Save",
        Command,
        function (data, status) {
            //alert("Data: " + data + "\nStatus: " + status);
        });



}


function CloneRecord(that, id) {

    var Command = getValues(id);



    $.post("/command/Clone",
        Command,
        function (data, status) {
            //alert("Data: " + data + "\nStatus: " + status);
        });



}



function GroupButtons(value) {


    var template = $('#CommandButtons').html();

    
    var html = Mustache.to_html(template, value);
    return html;
}

function EditDetail(a)
{

    that = $(a)
    that.children().first().css('display', 'table-cell');
    

}
function EditCar(num, type, orentation, id)
{
     ret = '<div class="position">'
    ret += '<div class="rawvalue">'
    ret += '<span class="orentation">' + orentation+'</span>'
    
    ret += '<input id="' + type+orentation+id+'" class="dataPoints" data-type="' + type + '" data-orentation="' + orentation + '" type="text" value="' + parseFloat(num).toFixed(5) + '"/>'
    ret += '</div>'

    ret += '<div class="adjustGroup">'
    ret += adjustHTML('dm')
    ret += adjustHTML('cm')
    ret += adjustHTML('mm')
    ret += adjustHTML('nm')
    ret += '</div>'
    ret += '</div>'
    return ret
}
function adjustHTML(measure)
{
    ret = '<div class="adjuster"><span class="arowInfo">' + measure + '</span><i class="fa fa-arrow-up" data-measure="' + measure + '" onclick="adjust(this, 1)" aria-hidden="true"></i><i class="fa fa-arrow-down" data-measure="' + measure +'" onclick="adjust(this, -1)" aria-hidden="true"></i></div>'
    return ret;

}

function adjust(a, way)
{
    that = $(a)

    adjustGroup = that.closest(".adjustGroup").prev()
   

    dataPoint = adjustGroup.find(".dataPoints")
   

    measure = that.data('measure')
   
    incriment = 0.0;
    switch (measure)
    {
        case 'mm':
            incriment = .001 * way
            break;
        case 'nm':
            incriment = .0001 * way
            break;
        case 'cm':
            incriment = .01 * way
            break;
        case 'dm':
            incriment = .1 * way
            break;


    }
    
    val = dataPoint.val()
    newval = parseFloat(val) + parseFloat(incriment)
 
    dataPoint.val(newval.toFixed(5));
}