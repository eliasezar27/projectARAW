$(document).ready(function() {

    $(document).on(
        {'click': function() {

            var section_id = $(this).attr('section_id');
            var student_id = $(this).attr('student_id');
            var action = $(this).attr('action');
            var reason = $('#declineDescription').val();

            req = $.ajax({
                url : '/request/action',
                type : 'POST',
                data : {
                        section_id : section_id,
                        student_id : student_id,
                        action : action,
                        reason: reason
                        }
            });

            console.log(section_id);
            console.log(action);

            req.done(function(data) {

                if (data.result == 'success'){
                    console.log(data.result);
                    $('#incomingStudentListContainer').load(location.href + " #incomingStudentList" );
                }else{
                    console.log(data.result);
                }

                if(data.action == 1){
                    $('#requestStatusAlert').html('');
                    $('#requestStatusAlert').removeClass('alert-warning');
                    $('#requestStatusAlert').addClass('alert-success');
                    $('#requestStatusAlert').html('Request Accepted');
                    console.log('accept');
                }else{
                    $('#requestStatusAlert').html('');
                    $('#requestStatusAlert').removeClass('alert-success');
                    $('#requestStatusAlert').addClass('alert-warning');
                    $('#requestStatusAlert').html('Request Declined');
                    $('#declineStudentModal').modal('toggle');
                    console.log('decline');
                }

                $('#requestStatusAlert').fadeIn('slow', function(){
                   $('#requestStatusAlert').delay(4000).fadeOut();
                });

            });


        }
    }, '.acceptRequestButton, .rejectRequestButton');

});