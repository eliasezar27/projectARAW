 $(document).ready(function(){
    $("#student").prop("disabled", true);
    $("#student").css({"opacity": "100%"});
    $("#teacher").css({"opacity": "40%"});

    $("#student").click(function(){
        $("#form-owner").val("student");
        $(this).prop("disabled", true);
        $(this).css({"opacity": "100%"});
        $("#teacher").prop("disabled", false);
        $("#teacher").css({"opacity": "40%"});
    });

    $("#teacher").click(function(){
        $("#form-owner").val("teacher");
        $(this).prop("disabled", true);
        $(this).css({"opacity": "100%"});
        $("#student").prop("disabled", false);
        $("#student").css({"opacity": "40%"});
    });

});