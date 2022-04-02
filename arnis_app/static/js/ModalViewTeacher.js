$(document).ready(function() {

    $(document).on(
        {'click': function() {

            var teacher_id = $(this).attr('teacher_id');

            console.log(teacher_id);

            req = $.ajax({
                url : '/view/teacher',
                type : 'GET',
                data : {
                        teacher_id : teacher_id
                        }
            });

                req.done(function(data) {

                    var teacherModalHeader = function(x,y) {
                        if(y['middle_name'] != ""){
                                x.html(y['last_name'] + ', ' + y['first_name'] + ' ' + y['middle_name']);
                           }else{
                                 x.html(y['last_name'] + ', '  + y['first_name']);
                           }
                    };

                    var my_date_format = function(input){
                        var d = new Date(Date.parse(input.replace(/-/g, "/")));
                        var month = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
                        var date = d.getDate() + ", " + month[d.getMonth()] + " " + d.getFullYear();
                        var time = d.toLocaleTimeString().toLowerCase().replace(/([\d]+:[\d]+):[\d]+(\s\w+)/g, "$1$2");
                        return (date + " " + time);
                    };

                    var teacherModalInfo = function(x,y) {
                      x.html(
                            "<div id='gender'> Sex: " + y['gender'] + "</div>"+
                            "<div id='email'>Email: " + y['email'] + "</div>"+
                            "<div id='mobile'>Contact Number: " + y['mobile'] + " </div>"+
                            "<div id='date_joined'>Date joined: " + my_date_format(y['date_joined']) + "</div>" );
                    };

                    if (data.result == 'success'){
                        teacherModalHeader($('#teacherMoreInfoModalHeader'), data.teacherInfo);
                        teacherModalInfo($("#teacherMoreInfoModalBody"), data.teacherInfo);
                        $('input:radio[name=userStatus]').attr('user_id', data.teacherInfo['user_id']);

                        // Setting which active status button is selected
                        if(data.teacherInfo['active'] == true){
                            $("#statusActive").prop("checked", true);
                        }else{
                            $("#statusInactive").prop("checked", true);
                        }

                    }else{
                        $('#ModalTeacherName').html('No records found!');
                    }

                console.log(data.result);

            });


        }
    }, '.viewTeacherInfo');

});