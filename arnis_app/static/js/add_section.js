$(document).ready(function() {

    $('#add_section').on('click', function() {

        var section_num = $('#sectionNumber').val();
        var trackID = $('#trackID').val();
        var strandID = $('#strandID').val();
        var teacherID = $('#teacherID').val();

        req = $.ajax({
            url : '/add_section',
            type : 'POST',
            data : {
                    section_num : section_num,
                    trackID : trackID,
                    strandID : strandID,
                    teacherID : teacherID
                    }
        });

        req.done(function(data) {

            if (data.result == 'success'){
                $('#addResult').append(data.result);

                $('#sectionNumber').val(null);
                $('#trackID').val(0);
                $('#strandID').val(0);
                $('#teacherID').val(0);

                $('#sectionList').load(window.location.href + " #sectionList" );

            }else{
                $('#addResult').toggleClass('alert-success alert-danger').append(data.result);
            }

            $('#addResult').fadeIn('slow', function(){
               $('#addResult').delay(3000).fadeOut();
            });



            console.log(data.result);

        });


    });

});