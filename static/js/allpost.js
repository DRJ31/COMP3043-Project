$(document).ready(function () {
    var total = 20;
    var finish = false;
    $(document).scroll(function () {
        if ($(document).scrollTop() + window.innerHeight === $(document).height()) {
            if (!finish) {
                $.get('/getmore/', {start: total, length: length}, function (data) {
                    data = JSON.parse(data);
                    var arr = data['result'];
                    if (arr.length === 0) {
                        finish = true;
                        return;
                    }
                    printHTML(arr);
                });
                total += 20;
            }
        }
    });
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


function printHTML(arr) {
    var str = "";
    for (var i = 0; i < arr.length; i++) {
        str += '<li class="list-group-item">\n' +
            '<div class="row">\n' +
            '<div class="col-4 col-md">' +
            arr[i][0];
        if (arr[i][1] === 'F')
            str += ' <span class="badge badge-info">Found</span>';
        else
            str += ' <span class="badge badge-warning">Lost</span>';
        str += '</div>\n' +
            '<div class="col-4 col-md">' + arr[i][2] + '</div>\n' +
            '<div class="col-4 col-md">' + arr[i][3] + '</div>\n' +
            '<div class="col options">\n' +
            '<a href="/detail/' + arr[i][5] + '">' +
            '<button class="btn btn-sm btn-secondary">Detail</button>' +
            '</a>\n' +
            '<button class="btn btn-sm btn-danger btn-delete" data-toggle="modal" data-target="#confirm-delete-modal" onclick="get_data(this)">' +
            'Delete' +
            '</button>' +
            '</div>\n' +
            '</div>\n' +
            '</li>';
    }
    $("#mainTable").append(str);
}


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

function get_data(obj) {
    var id = $(obj).parent().find('a')[0].href.split("/")[4];
    $.post('/getkey/', {
        id: id
    }, function (data) {
        $("#delete-link").attr('href', "/delete/" + data);
    });
}