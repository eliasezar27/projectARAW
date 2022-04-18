 $( document ).ready(function(){
    $('.alert').not('#addResult, #editTrackResult, #addStrandResult, #transferStudentResult, .student, #requestStatusAlert, #remNote').fadeIn('slow', function(){
       $('.alert').not('#addResult, #editTrackResult, #addStrandResult, #transferStudentResult, .student, #requestStatusAlert, #remNote').delay(7000).fadeOut();
    });
});