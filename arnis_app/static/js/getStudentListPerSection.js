$(document).ready(function() {

    $(document).on(
        {'click': function() {

            var section_id = $(this).attr('section_id');

            req = $.ajax({
                url : '/view/student/list',
                type : 'GET',
                data : {
                        section_id : section_id
                        }
            });

                req.done(function(data1) {

                    if (data1.result == 'success'){
                        for (let i = 0; i < data1.listStudents.length; i++){
                            data1.listStudents[i]['actions'] = "<a class='transferStudent px-2 py-2' student_id=" + data1.listStudents[i]['student_id'] + " style='cursor: pointer; text-decoration: none;' data-bs-toggle='modal' data-bs-target='#transferStudentModal'>"+
                                                                    "<i class='fas fa-solid fa-arrow-right-from-bracket' data-bs-toggle='tooltip' data-bs-placement='top' title='Transfer student' style='color: #c46d38;'></i>" +
                                                                "</a>"
                        }
//                        console.log(data1.sectionList);
//                        console.log(data1.teacherInfo);
                        console.log(data1.result);
                        $('#sectionStudentListTable').bootstrapTable('load', data1.listStudents);
                    }else{
                        console.log(data1.result);
                    }

            });


        }
    }, '.viewSectionStudentList');

});