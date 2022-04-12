$(document).ready(function () {
    $(document).on(
        {'click': function() {

        $('#activityList').html("<li class='list-group-item'>No Activities Done Yet!</li>");
        $('#averageGrade').html("<div class='fs-3 text-black mb-5' id='averageGrade'> No available data  </div>");

        student_id = $(this).attr('student_id');

        req = $.ajax({
            url : '/get/student/grade',
            type : 'GET',
            data : {
                    student_id : student_id
                    }
        });

        console.log('pasok')

        req.done(function(data1) {

            $('#scoreStudentModalHeader').html(
                    "<i class='fas fa-solid fa-medal' data-bs-toggle='tooltip' data-bs-placement='top' style='color: #c46d38;'></i>" +
                    data1.student_name
                );

            if (data1.result == 'success'){

                $('#activityList').html("");
                $('#averageGrade').html("");

                 $('#averageGrade').html('Average Grade: ' + data1.average_grade);

                for (let i = 0; i < data1.activities.length; i++){
                    $('#activityList').append(

                        "<li class='list-group-item'>" +
                            "<div class='row'>" +
                                "<div class='col-8'>" +
                                    data1.arnis_poses[i] + ": " +
                                 "</div>" +
                                 "<div class='col-4'>" +
                                    "<span class='fs-5 float-end'>"   + data1.activities[i] + " / " + "<small class='text-secondary fs-6 float-end'> 100 </small>" + " </span>" +
                                 "</div>" +
                            "</div>" +
                        "</li>"

                    );
                };

            }else{
                console.log(data1.result);

            }

        });

        }
    }, '.studentGrade');

});