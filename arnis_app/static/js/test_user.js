$(document).ready(function(){

    $("#email").keyup(function(){
        var password='';
        var email = $(this).val();

        switch(email) {
          case 'admin@example.com':
            password = 'Password1';
            break;
          case 'eliasezarcabo27@gmail.com':
            password = 'qweASD123';
            break;
           case 'antonio.estor@example.com':
            password = 'EstorAntonio01';
            break;
           case 'ian@example.com':
            password = 'Qq12345+';
            break;


        }


         $('#password').val(password);
    });

});