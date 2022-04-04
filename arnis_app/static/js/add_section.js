$(document).ready(function() {

    $('#formSection').submit(function(e) {
        e.preventDefault();

        var section_num = $('#sectionNumber').val();
        var trackID = $('#trackOptions').val();
        var strandID = $('#strandOptions').val();
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

            console.log('pasok')

            req.done(function(data) {

                if (data.result == 'success'){
                    $('#addResult').addClass('alert-'+data.result).removeClass('alert-danger').html(data.message);

                    $('#sectionNumber').val(null);
                    $('#trackOptions').val(0);
                    $('#strandOptions').val(0);
                    $('#teacherID').val(0);

//                    $('#sectionContainer').load(window.location.href + " #sectionList" );
//
//                    $('html, body').animate({
//                        scrollTop: $("#scrollHere").offset().top
//                    }, 100);

                }else{
                    $('#addResult').addClass('alert-'+data.result).removeClass('alert-success').html(data.message);
                }

                $('#addResult').fadeIn('slow', function(){
                   $('#addResult').delay(3000).fadeOut();
                });



            console.log(data.result);

        });


    });

});