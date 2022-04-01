$(document).ready(function() {

    $(document).on(
        {'change': function() {

            var user_id = $(this).attr('user_id');
            var userStatus = $(this).val();

            console.log(user_id);
            console.log('pasok');

            req = $.ajax({
                url : '/change/user/status',
                type : 'POST',
                data : {
                        user_id: user_id,
                        userStatus: userStatus
                        }
            });

                req.done(function(data) {

                   console.log(data.success)

            });


        }
    }, 'input:radio[name=userStatus]');

});