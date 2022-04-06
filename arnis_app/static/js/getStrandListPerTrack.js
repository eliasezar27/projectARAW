$(document).ready(function() {

    $(document).on(
        {'click': function() {

            var track_id = $(this).attr('track_id');

            req = $.ajax({
                url : '/view/strand/list',
                type : 'GET',
                data : {
                        track_id : track_id
                        }
            });

                req.done(function(data1) {

                    if (data1.result == 'success'){
//                        for (let i = 0; i < data1.sectionList.length; i++){
//                            data1.sectionList[i]['actions'] = "<a class='viewSectionStudentList px-2 py-2' section_id=" + data1.sectionList[i]['section_id'] + " style='cursor: pointer; text-decoration: none;' data-bs-toggle='modal' data-bs-target='#sectionStudentList'>"+
//                                                                    "<i class='fas fa-solid fa-user-group' data-bs-toggle='tooltip' data-bs-placement='top' title='More Info..' style='color: #c46d38;'></i>" +
//                                                                "</a>"
//                        }
//                        console.log(data1.sectionList);
//                        console.log(data1.teacherInfo);
                        console.log(data1.result);
                        $('#strandListTable').bootstrapTable('load', data1.strand_list);
                    }else{
                        console.log(data1.result);
                    }

            });


        }
    }, '.viewTrack');

});