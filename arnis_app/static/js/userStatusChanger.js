$(document).ready(function() {

    $(document).on(
        {'change': function() {
            $('#statChangeFlash').removeClass('alert-success').html('');
            $('#statChangeFlash').removeClass('alert-danger').html('');

            var user_id = $(this).attr('user_id');
            var userStatus = $(this).val();

            console.log(user_id);

            req = $.ajax({
                url : '/change/user/status',
                type : 'POST',
                data : {
                        user_id: user_id,
                        userStatus: userStatus
                        }
            });

                req.done(function(data) {

                    if(data.status == 0){
                        $('#statChangeFlash').addClass('alert-danger').html('User is set to Inactive');
                    }else{
                        $('#statChangeFlash').addClass('alert-success').html('User is set to Active');
                    }

                    $('#statChangeFlash').fadeIn('slow', function(){
                        $('#statChangeFlash').delay(3000).fadeOut();
                });

            });


        }
    }, 'input:radio[name=userStatus]');

});