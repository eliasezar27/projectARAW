$(document).ready(function() {

    $(document).on(
        {'change': function() {
            $('#statChangeFlash').removeClass('alert-success').html('');
            $('#statChangeFlash').removeClass('alert-danger').html('');

            var user_id = $(this).attr('user_id');
            var adminStatus = $(this).prop("checked");

            if (adminStatus == true){
                adminStatus = 1;
            }else{
                adminStatus = 0;
            }

            console.log(user_id);
            console.log(adminStatus);

            req = $.ajax({
                url : '/assign/admin',
                type : 'POST',
                data : {
                        user_id: user_id,
                        adminStatus: adminStatus
                        }
            });

            req.done(function(data) {

                if(data.status == 0){
                    $('#statChangeFlash').addClass('alert-danger').html('User unassigned as Admin');
                }else{
                    $('#statChangeFlash').addClass('alert-success').html('User assigned as Admin');
                }

                $('#statChangeFlash').fadeIn('slow', function(){
                    $('#statChangeFlash').delay(3000).fadeOut();
                });

            });


        }
    }, 'input:checkbox[id=setAdminSwitch]');

});