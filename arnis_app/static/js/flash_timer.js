 $( document ).ready(function(){
    $('.alert').not('#addResult').fadeIn('slow', function(){
       $('.alert').not('#addResult').delay(3000).fadeOut();
    });
});