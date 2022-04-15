 $( document ).ready(function(){
    $('.alert').not('#addResult, #editTrackResult, #addStrandResult, #transferStudentResult, .student').fadeIn('slow', function(){
       $('.alert').not('#addResult, #editTrackResult, #addStrandResult, #transferStudentResult, .student').delay(7000).fadeOut();
    });
});