$(document).ready(function() {

    $(document).on(
        {'click': function() {

            var name = $(this).attr('pose_name');
            var img = $(this).attr('pose_img');
            var img_holder = $('#imageHolder img').attr('src');
            var desc = $('p', this).text();
            var address = $('b', this).text();
            address = address.trim()

            $('#poseDescriptionHeader span').text(name);
            $('#imageHolder img').attr('src', img_holder.slice(0, 21) + img);
            $('#descHolder p').text(desc);
            $('#watchVidDemo').attr('address', address);



        }
    }, '.viewPoseDescriptionListLink');

});