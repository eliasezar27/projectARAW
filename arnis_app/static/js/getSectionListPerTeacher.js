$(document).ready(function() {

    $(document).on(
        {'click': function() {

            var teacher_id = $(this).attr('teacher_id');

            req = $.ajax({
                url : '/view/section/list',
                type : 'GET',
                data : {
                        teacher_id : teacher_id
                        }
            });

                req.done(function(data1) {

//                                Action to View Handled Sections List Modal
                                <a class="viewStudentList px-1" teacher_id="{{teach[0].teacher_id}}" style="cursor: pointer; text-decoration: none;" data-bs-toggle="modal" data-bs-target="#teacherSectionListModal">
                                    <i class="fas fa-solid fa-users" data-bs-toggle="tooltip" data-bs-placement="top" title="Sections handled" style="color: #c46d38;"></i>
                                </a>

//                                Action to View Teacher Info Modal
                                <a class="viewTeacherInfo px-1" teacher_id="{{teach[0].teacher_id}}" style="cursor: pointer; text-decoration: none;" data-bs-toggle="modal" data-bs-target="#teacherMoreInfoModal">
                                    <i class="fas fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="More Info.." style="color: #EDB518;"></i>
                                </a>

                    if (data1.result == 'success'){
//                        console.log(data1.sectionList);
                        console.log(data1.result);
                        $('#teacherSectionListTable').bootstrapTable('load', data1.sectionList);
                    }else{
                        console.log(data1.result);
                    }

            });


        }
    }, '.viewTeacherSection');

});