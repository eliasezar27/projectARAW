$(document).ready(function() {

    $('#reassign_confirm').click(function() {

        var student_id = $(this).attr('student_id');

        console.log(student_id);

        req = $.ajax({
            url : '/reassign/student',
            type : 'POST',
            data : {
                    student_id : student_id,
                    }
        });

        req.done(function(data) {

            if (data.result == 'success'){

                location.reload();

                console.log(data.result + ': ' + data.message);

            }else{
                console.log(data.result + ': ' + data.message);
            }

        });


    });

});