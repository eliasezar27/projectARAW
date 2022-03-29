$(document).ready(function() {
    $("#profilePic").css('cursor', 'pointer');
    $("#imageUpload").css('display', 'none');
    $("#profilePic").on('click', function() {
        $("#imageUpload").click();
    });

    imageUpload.onchange = evt => {
      const [file] = imageUpload.files
      if (file) {
        profilePic.src = URL.createObjectURL(file)
      }
    }

});