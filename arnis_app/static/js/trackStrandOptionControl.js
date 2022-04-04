$(document).ready(function () {
    $("select#strandOptions option").show();

    $('#trackOptions').on('change', function() {
        $("select#strandOptions option").show();
        $("select#strandOptions option:not([name="+$(this).val()+"])").hide();
    });
});