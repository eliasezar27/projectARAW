$(document).ready(function() {

    $('#teacherRefresh').on('click', function(e) {
        $('#teacherContainer').load(window.location.href + " #teacherList ");
        console.log("teacher refresh");
    });
});