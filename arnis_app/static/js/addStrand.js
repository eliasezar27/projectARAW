$(document).ready(function() {

    $('#addStrandForm').submit(function(e) {
        e.preventDefault();

        var track_id = $('#trackOptions').val();
        var strand_name = $('#addStrandName').val();
        var strand_nickname = $('#addStrandNickname').val();

        req = $.ajax({
            url : '/add_strand',
            type : 'POST',
            data : {
                    track_id : track_id,
                    strand_name : strand_name,
                    strand_nickname : strand_nickname
                    }
        });

        console.log('pasok')

        req.done(function(data) {

            if (data.result == 'success'){
                $('#addStrandResult').addClass('alert-'+data.result).removeClass('alert-danger').html(data.message);

                $('#trackListMainContainer').load(location.href + " #trackListContainer" );

            }else{
                $('#addStrandResult').addClass('alert-'+data.result).removeClass('alert-success').html(data.message);
            }

            $('#addStrandResult').fadeIn('slow', function(){
               $('#addStrandResult').delay(3000).fadeOut();
            });

            console.log(data.result);

        });


    });

});