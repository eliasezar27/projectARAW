$(document).ready(function(){

    $("#defaultCheck1").change(function(){
         if($(this).is(':checked')){
            $('#password').attr('type', 'text');
            $('#repassword').attr('type', 'text');
         }else{
            $('#password').attr('type', 'password');
            $('#repassword').attr('type', 'password');
         }
    });

 });