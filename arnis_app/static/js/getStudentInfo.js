$(document).ready(function() {

    $(document).on(
        {'click': function() {

            var student_id = $(this).attr('student_id');

            req = $.ajax({
                url : '/get/student/info',
                type : 'GET',
                data : {
                        student_id : student_id
                        }
            });

                req.done(function(data1) {

                    if (data1.result == 'success'){
                        $('#student_id').val(data1.student_info['last_name'] + ', ' + data1.student_info['first_name']);
                        $('#student_id').attr('student_id', data1.student_info['student_id']);
                        console.log(data1.result);
                    }else{
                        console.log(data1.result);
                    }

            });


        }
    }, '.transferStudent');

});