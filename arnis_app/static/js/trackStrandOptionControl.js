$(document).ready(function () {
    $("select#strandOptions option").show();
    $("select#strandOptions option:not([name="+$('#trackOptions').val()+"])").hide();
    $("select#strandOptions option[value='0']").show();

    $('#trackOptions').on('change', function() {
        $("select#strandOptions option").hide();
        $("select#strandOptions option[name="+$(this).val()+"]").show();
        $("select#strandOptions option[value='0']").show();
    });

});