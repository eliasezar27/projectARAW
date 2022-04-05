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

                req.done(function(data) {

                    function pad(num, size) {
                        num = num.toString();
                        while (num.length < size) num = "0" + num;
                        return num;
                    }

                    if (data.result == 'success'){
//                        console.log(data.listStudents);
                         $('#sectionStudentListModalHeader').html(pad(data.sectionInfo['section_no'], 2) + ' - ' + data.sectionInfo['strand_nickname']);
                         $('#studentListTable').bootstrapTable('load', data.listStudents);


                    }else{
                        console.log(data.result);
                    }

            });


        }
    }, '.viewSectionStudentList');

});