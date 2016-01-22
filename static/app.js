$(document).ready(function(){
    // the socket.io documentation recommends sending an explicit package upon connection
    // this is specially important when using the global namespace
    var socket = io.connect('http://' + document.domain + ':' + location.port);

    // event handler for server sent data
    // the data is displayed in the "Received" section of the page
    var row_no = 0;

    socket.on('my response', function(msg) {
        var holder = $('#console');

        // Viewer advised, ugly solution follows... I was bored

        var html_style = '';
        if(msg.color != undefined) {
            html_style = 'style="color: ' + msg.color + '"'
        }

        var html = '<div id="crown' + row_no +'" class="crow "' + html_style +'>';

        if(msg.ip != undefined) {
            html += '[' + msg.ip + '] ';
        }

        if(msg.name != undefined) {
            html += '[' + msg.name + '] ';
        }

        html += msg.msg;

        html += '</div>';

        holder.append(html);

        // I don't know why is that 41px there, it should have been 1...
        if (holder.prop('scrollHeight') - holder.prop('clientHeight') <= holder.scrollTop() + 41) {
            holder.scrollTop(holder.prop("scrollHeight"));
        }

        row_no++;
    });

    // event handler for new connections
    socket.on('connect', function() {
        socket.emit('my event', {data: 'socket.io Connected'});
    });

    // handlers for the different forms in the page
    // these send data to the server in a variety of ways1
    $('form#emit').submit(function(event) {
        socket.emit('my event', {data: $('#emit_data').val()});
        return false;
    });
    $('form#disconnect').submit(function(event) {
        socket.emit('disconnect request');
        return false;
    });

    // Adjust div#console size to always be placed at the bottom of window
    updateConsoleSize();
    $(window).resize(function() {
        updateConsoleSize();
    });

    $('#console').on('click','.crow', function () {
        $(this).parent().find('.crow').css('background-color', '');
        $(this).css('background-color', '#424124');
    });

});

function updateConsoleSize() {
    $('#console').height(function(index, height) {
        return window.innerHeight - $(this).offset().top - parseInt($(this).css('padding-top')) - parseInt($(this).css('padding-bottom'));
    });
}
