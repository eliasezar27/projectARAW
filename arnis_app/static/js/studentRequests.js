$(document).ready(function() {

    $(document).on(
        {'click': function() {

            var section_id = $(this).attr('section_id');
            var student_id = $(this).attr('student_id');
            var action = $(this).attr('action');

            req = $.ajax({
                url : '/request/action',
                type : 'POST',
                data : {
                        section_id : section_id,
                        student_id : student_id,
                        action : action
                        }
            });

            console.log(section_id);
            console.log(action);

            req.done(function(data) {

                if (data.result == 'success'){
                    console.log(data.result);
                    $('#joinRequestCardContainer').load(location.href + " #joinRequestCard" );
                }else{
                    console.log(data.result);
                }

            });


        }
    }, '.acceptRequestButton, .rejectRequestButton');

});