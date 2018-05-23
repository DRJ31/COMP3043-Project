$(document).ready(function () {
    $("#photo").fileinput({
        theme: "fas",
        showUpload: false
    });
    $("#icon-close, #btn-close").click(function () {
        $("#post-detail")[0].reset();
    });
    $("#post").click(function () {
        if (!checkForm()) {
            $("#alert-msg").addClass("alert-danger").html("Please finish the form.");
            return;
        }
        $("#post-detail").ajaxSubmit({
            success: function () {
                $("#alert-msg").removeClass('alert-danger').addClass("alert-success");
                $("#close-msg").addClass('d-none');
                $("#refresh").removeClass('d-none');
                pageRefresh();
            },
            error: function () {
                $("#alert-msg").removeClass("alert-success").addClass("alert-danger").html("Error, please try again.");
            }
        });
    });
    $("#close-msg").click(function () {
        $("#alert-msg").removeClass("alert-success alert-danger").html("");
    });
    $("#refresh").click(function () {
        location.reload();
    });
});

function checkForm() {
    var status = true;
    if ($("#objectName").val() === "") {
        $("#objectName").removeClass("is-valid").addClass("is-invalid");
        status = false;
    }
    else
        $("#objectName").removeClass('is-invalid').addClass("is-valid");
    $("#status-type").addClass("is-valid");
    if ($("#location").val() === "") {
        $("#location").removeClass("is-valid").addClass("is-invalid");
        status = false;
    }
    else
        $("#location").removeClass("is-invalid").addClass("is-valid");
    if ($("#location").val() === "") {
        $("#location").removeClass("is-valid").addClass("is-invalid");
        status = false;
    }
    else
        $("#location").removeClass("is-invalid").addClass("is-valid");
    if ($("#description").val() === "") {
        $("#description").removeClass("is-valid").addClass("is-invalid");
        status = false;
    }
    else
        $("#description").removeClass("is-invalid").addClass("is-valid");
    if ($("#contact").val() === "") {
        $("#contact").removeClass("is-valid").addClass("is-invalid");
        status = false;
    }
    else
        $("#contact").removeClass("is-invalid").addClass("is-valid");
    if (!$("#default-photo")[0].checked) {
        if ($("#photo").val() === "") {
            $("#photo").removeClass("is-valid").addClass("is-invalid");
            status = false;
        }
        else
            $("#photo").removeClass("is-invalid").addClass("is-valid");
    }
    return status;
}

function pageRefresh() { //Refresh the page in 3s
    $("#alert-msg").html("You have successfully post! The page will refresh in 3 seconds.");
    setTimeout(function () {
        location.reload();
    }, 3000);
}