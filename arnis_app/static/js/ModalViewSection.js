$(document).ready(function() {

    $(document).on(
        {'click': function() {

            console.log('clicked');

            var section_id = $(this).attr('section_id');

            req = $.ajax({
                url : '/view/student/list',
                type : 'POST',
                data : {
                        section_id : section_id
                        }
            });

                req.done(function(data) {

                    $('#dataTableSectionList').bootstrapTable({
                        pagination: true,
                        search: true,
                    });

                    function pad(str, max) {
                      str = str.toString();
                      return str.length < max ? pad("0" + str, max) : str;
                    }

                    var sectionListModalHeader = function(x,y) {
                      x.html(pad(y['section_no'], 2) + '-' + y['strand_nickname']);
                    };

                    var sectionListModalInfo = function(x,y) {
                      x.html("<div class='card card-body'>" +
                            "<div id='population'><strong>Number of Students:</strong> " + y['population'] + "</div>"+
                            "<div id='track'><strong>Track:</strong> " + y['track_name'] + "</div>"+
                            "<div id='strand'><strong>Strand:</strong> " + y['strand_name'] + " </div>"+
                            "<div id='teacher'><strong>Assigned to:</strong> " + y['last_name'] + ", " + y['first_name'] + " " + y['middle_name'] + "</div>"+
                          "</div>" );
                    };

                    console.log(data.listStudents);

                    if (data.result == 'single'){
                        console.log('Section info');
                        sectionListModalHeader($('#modalSectionName'), data.sectionInfo);
                        sectionListModalInfo($("#collapseSectionInfo"), data.sectionInfo);
                        var studentList = [];
                    }else if(data.result == 'both'){
                        console.log('Section info and student list');
                        sectionListModalHeader($('#modalSectionName'), data.sectionInfo);
                        sectionListModalInfo($("#collapseSectionInfo"), data.sectionInfo);
                        var studentList = data.listStudents;

                    }else{
                        $('#modalSectionName').html('No records found!');
                        var studentList = [];
                    }

                    $('#dataTableSectionList').bootstrapTable("load", studentList);

                console.log(data.result);

            });


        }
    }, '.viewSection');

});