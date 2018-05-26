$(document).ready(function () {
    $("#confirmPass").bind('input', function () {
        if ($("#confirmPass").val() !== $("#newPass").val()) {
            $("#change").attr('disabled', 'disabled');
        }
        else {
            $("#change").removeAttr('disabled');
        }
    });
});