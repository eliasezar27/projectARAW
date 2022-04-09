$(document).ready(function() {

    $(document).on(
        {'click': function() {

            var address = $(this).attr('address');
            var poseName = $('#poseDescriptionHeader span').text();
            
            $('#videoModalBody').html("<iframe height='500' src='https://www.youtube.com/embed/" + address + "?autoplay=1&controls=0&loop=1&mute=1&playlist=" + address + "' class='px-5 mx-5'></iframe>");

            console.log("<iframe height='500' src='https://www.youtube.com/embed/" + address + "?autoplay=1&controls=0&loop=1&mute=1&playlist=" + address + "' class='px-5 mx-5'></iframe>");

            $('#videoModalHeader h5').text(poseName);

        }
    }, '#watchVidDemo');

});