$(document).ready(function() {

    $(document).on(
        {'click': function() {

            var student_id = $(this).attr('student_id');

            req = $.ajax({
                url : '/save/grade',
                type : 'POST',
                data : {
                        student_id: student_id
                        }
            });

                req.done(function(data) {

                    if(data.result == 'success'){
                        console.log('grade recorded');
                    }else{
                        console.log('something went wrong');
                    }

            });


        }
    }, '#saveGrade');

});