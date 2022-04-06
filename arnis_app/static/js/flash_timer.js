 $( document ).ready(function(){
    $('.alert').not('#addResult, #editTrackResult, #addStrandResult').fadeIn('slow', function(){
       $('.alert').not('#addResult, #editTrackResult, #addStrandResult').delay(3000).fadeOut();
    });
});