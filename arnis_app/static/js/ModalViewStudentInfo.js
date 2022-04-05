$(document).ready(function() {

    $(document).on(
        {'click': function() {

            var student_id = $(this).attr('student_id');

            req = $.ajax({
                url : '/view/student/info',
                type : 'GET',
                data : {
                        student_id : student_id
                        }
            });

                req.done(function(data) {

                    function pad(num, size) {
                        num = num.toString();
                        while (num.length < size) num = "0" + num;
                        return num;
                    }

                    var studentModalHeader = function(x,y) {
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

                    var studentModalInfo = function(x,y, z) {
                          if (y['section_id'] != null){
                          x.html(

                                "<div id='gender'> Sex: " + y['gender'] + "</div>"+
                                "<div id='email'>Email: " + y['email'] + "</div>"+
                                "<div id='mobile'>Contact Number: " + y['mobile'] + " </div>"+
                                "<div id='date_joined'>Date joined: " + my_date_format(y['date_joined']) + "</div>" +
                                "<hr>" +
                                "<div class='text-black'>" +
                                    "<i class='fas fa-solid fa-user-group' data-bs-toggle='tooltip' data-bs-placement='top' title='More Info..' style='color: #c46d38;'></i>" +
                                     " " + pad(z['section_no'], 2) + ' - ' + z['strand_nickname'] +
                                "</div>" +
                                "<div>Teacher: "  + z['last_name'] + ", " + z['first_name'] + "</div>" +
                                "<div>Track: "  + z['track_name'] + "</div>" +
                                "<div>Strand: "  + z['strand_name'] + "</div>"
                                );
                          }else{
                          x.html(
                                "<div id='gender'> Sex: " + y['gender'] + "</div>"+
                                "<div id='email'>Email: " + y['email'] + "</div>"+
                                "<div id='mobile'>Contact Number: " + y['mobile'] + " </div>"+
                                "<div id='date_joined'>Date joined: " + my_date_format(y['date_joined']) + "</div>"  +
                                 "<hr>" +
                                 "<div class='text-center'> No Section joined yet</div>"

                                );
                                }
                    };

                    if (data.result == 'success'){
                        console.log(data.studentInfo['section_id']);
                        studentModalHeader($('#studentMoreInfoModalHeader'), data.studentInfo);
                        studentModalInfo($("#studentMoreInfoModalBody"), data.studentInfo, data.studentSectionInfo);
                        $('input:radio[name=userStatus]').attr('user_id', data.studentInfo['user_id']);

                        // Setting which active status button is selected
                        if(data.studentInfo['active'] == true){
                            $("#statusActive").prop("checked", true);
                        }else{
                            $("#statusInactive").prop("checked", true);
                        }

                    }else{
                        $('#studentMoreInfoModalHeader').html('No records found!');
                    }

                console.log(data.result);

            });


        }
    }, '.viewStudentInfo');

});