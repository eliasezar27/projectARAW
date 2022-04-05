$(document).ready(function() {

    $(document).on(
        {'change': function() {

            var teacher_id = $(this).attr('teacher_id');

            req = $.ajax({
                url : '/view/section/list',
                type : 'GET',
                data : {
                        teacher_id : teacher_id
                        }
            });

                req.done(function(data1) {

                    if (data1.result == 'success'){
                        for (let i = 0; i < data1.sectionList.length; i++){
                            data1.sectionList[i]['actions'] = "<a class='viewSectionStudentList px-2 py-2' section_id=" + data1.sectionList[i]['section_id'] + " style='cursor: pointer; text-decoration: none;' data-bs-toggle='modal' data-bs-target='#sectionStudentList'>"+
                                                                    "<i class='fas fa-solid fa-user-group' data-bs-toggle='tooltip' data-bs-placement='top' title='More Info..' style='color: #c46d38;'></i>" +
                                                                "</a>"
                        }
//                        console.log(data1.sectionList);
//                        console.log(data1.teacherInfo);
                        console.log(data1.result);
                        $('#teacherSectionListTable').bootstrapTable('load', data1.sectionList);
                    }else{
                        console.log(data1.result);
                    }

            });


        }
    }, '.viewTeacherSection');

});