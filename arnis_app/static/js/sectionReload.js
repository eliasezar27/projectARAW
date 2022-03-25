$(document).ready(function() {

    $('#sectionRefresh').on('click', function(e) {
        $('#sectionContainer').load(location.href + " #sectionList" );
    });
});