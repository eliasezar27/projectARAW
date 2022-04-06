 $( document ).ready(function(){
    $('.alert').not('#addResult, #editTrackResult, #addStrandResult, #transferStudentResult').fadeIn('slow', function(){
       $('.alert').not('#addResult, #editTrackResult, #addStrandResult, #transferStudentResult').delay(3000).fadeOut();
    });
});