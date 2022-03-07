 $(document).ready(function(){
    $("#password, #repassword").keyup(function(){
        $("#createAcc").prop("disabled", false);
        $("#pass_message").css({"font-size": "12px"});

        if ($("#password").val() == '' ||  $("#repassword").val() == '') {
            $("#pass_message").css({"color": "none"});
            $("#pass_message").html("");
        } else if ($("#password").val() != $("#repassword").val()) {
            $("#pass_message").css({"color": "red"});
            $("#pass_message").html("Password do not match!");
            $("#createAcc").prop("disabled", true);
        } else if ($("#password").val() == $("#repassword").val()) {
            $("#pass_message").css({"color": "green"});
            $("#pass_message").html("Password match!");
        }
    });

});