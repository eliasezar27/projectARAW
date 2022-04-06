$(document).ready(function() {

    $('#editTrackForm').submit(function(e) {
        e.preventDefault();

        var track_id = $('#track_id').val();
        var track_name = $('#trackNameChange').val();
        var track_nickname = $('#trackNicknameChange').val();

        req = $.ajax({
            url : '/edit_track',
            type : 'POST',
            data : {
                    track_id : track_id,
                    track_name : track_name,
                    track_nickname : track_nickname
                    }
        });

        console.log('pasok')

        req.done(function(data) {

            if (data.result == 'success'){
                $('#editTrackResult').addClass('alert-'+data.result).removeClass('alert-danger').html(data.message);

                $('#trackListMainContainer').load(location.href + " #trackListContainer" );
                $('.viewTrackCard')[0].click();

            }else{
                $('#editTrackResult').addClass('alert-'+data.result).removeClass('alert-success').html(data.message);
            }

            $('#editTrackResult').fadeIn('slow', function(){
               $('#editTrackResult').delay(3000).fadeOut();
            });



        console.log(data.result);

        });


    });

});