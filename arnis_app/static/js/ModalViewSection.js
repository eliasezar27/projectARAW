$(document).ready(function() {

    $(document).on(
        {'click': function() {

            $('#sectionListTableBody').html('');

            var teacher_id = $(this).attr('teacher_id');

            req = $.ajax({
                url : '/view/section/list',
                type : 'GET',
                data : {
                        teacher_id : teacher_id
                        }
            });

                req.done(function(data1) {

                    var teacherModalHeader = function(x,y) {
                        if(y['middle_name'] != ""){
                                x.html('SECTIONS - ' + y['last_name'] + ', ' + y['first_name'] + ' ' + y['middle_name']);
                           }else{
                                 x.html('SECTIONS - ' + y['last_name'] + ', '  + y['first_name']);
                           }
                    };

                    if (data1.result == 'success'){
                        console.log(data1.sectionList);
                         teacherModalHeader($('#teacherSectionListModalHeader'), data1.teacherInfo);
                         $('#sectionListTable').bootstrapTable('load', data1.sectionList);


                    }else{
                        console.log(data1.result);
                    }

            });


        }
    }, '.viewSectionList');

});