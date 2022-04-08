$(document).ready(function() {

    $('#transferStudentForm').submit(function(e) {
        e.preventDefault();

        var student_id = $('#student_id').attr('student_id');
        var section_id = $('#sectionOptions').val();
        var reasonAction = $('#reasonTextArea').val();

        req = $.ajax({
            url : '/transfer/section',
            type : 'POST',
            data : {
                    student_id : student_id,
                    section_id : section_id,
                    reasonAction : reasonAction
                    }
        });

        console.log('pasok')

        req.done(function(data) {

            if (data.result == 'success'){
                $('#transferStudentResult').addClass('alert-'+data.result).removeClass('alert-danger').html(data.message);

            }else{
                $('#transferStudentResult').addClass('alert-'+data.result).removeClass('alert-success').html(data.message);
            }

            $('#transferStudentResult').fadeIn('slow', function(){
               $('#transferStudentResult').delay(3000).fadeOut();
            });

            console.log(data.result);

        });


    });

});