$(document).ready(function() {

    $(document).on(
        {'click': function() {

            console.log('pass');

            var teacher_id = $(this).attr('teacher_id');

            req = $.ajax({
                url : '/view/teacher',
                type : 'POST',
                data : {
                        teacher_id : teacher_id
                        }
            });

                req.done(function(data) {

                    $('#dataTableTeacherSection').bootstrapTable({
                        pagination: true,
                        search: true,
                    });

                    var teacherModalHeader = function(x,y) {
                      x.html(y['first_name'] + ' ' + y['middle_name'] + ' ' + y['last_name']);
                    };

                    var my_date_format = function(input){
                        var d = new Date(Date.parse(input.replace(/-/g, "/")));
                        var month = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
                        var date = d.getDate() + ", " + month[d.getMonth()] + " " + d.getFullYear();
                        var time = d.toLocaleTimeString().toLowerCase().replace(/([\d]+:[\d]+):[\d]+(\s\w+)/g, "$1$2");
                        return (date + " " + time);
                    };

                    var teacherModalInfo = function(x,y) {
                      x.html("<div class='card card-body'>" +
                            "<div id='gender'> Sex: " + y['gender'] + "</div>"+
                            "<div id='email'>Email: " + y['email'] + "</div>"+
                            "<div id='mobile'>Contact Number: " + y['mobile'] + " </div>"+
                            "<div id='date_joined'>Date joined: " + my_date_format(y['date_joined']) + "</div>"+
                          "</div>" );
                    };

                    if (data.result == 'single'){
                        teacherModalHeader($('#ModalTeacherName'), data.teacherInfo);
                        teacherModalInfo($("#collapseTeacherInfo"), data.teacherInfo);

                        var handledSection = [];
                    }else if(data.result == 'both'){
                        teacherModalHeader($('#ModalTeacherName'), data.teacherInfo);
                        teacherModalInfo($("#collapseTeacherInfo"), data.teacherInfo);

                        var handledSection = data.sectionList;
                    }else{
                        $('#ModalTeacherName').html('No records found!');
                        var handledSection = [];
                    }

                    $('#dataTableTeacherSection').bootstrapTable("load", handledSection);



                console.log(data.result);
                console.log(data.sectionList);

            });


        }
    }, '.viewTeacher');

});