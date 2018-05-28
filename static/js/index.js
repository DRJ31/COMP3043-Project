$(document).ready(function () {
    var total = 20;
    if ($(window).width() < 992) {
        $("#userMenu").attr("disabled", "disabled");
    }
    else {
        $("#userMenu").removeAttr("disabled");
    }
    $(window).resize(function () {
        if ($(window).width() < 992) {
            $("#userMenu").attr("disabled", "disabled");
        }
        else {
            $("#userMenu").removeAttr("disabled");
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
    $("#btn-search").click(function () {
        searching(null, 2, 0, 20);
    });
    $(document).keyup(function (e) {
        if (e.keyCode === 13 || $("#search").val().length === 0)
            searching(null, 2, 0, 20);
    });
    $(document).scroll(function () {
        if ($(document).scrollTop() + window.innerHeight === $(document).height()) {
            if ($("#numOfResults").html() > total) {
                load_more(total);
                total += 20;
            }
        }
    });
    $("#search").bind('input', function () {
        if ($("#search").val().length > 0)
            $("#btn-clear").removeClass('d-none');
        else
            $("#btn-clear").addClass('d-none');
    });
    $("#btn-clear").click(function () {
        $("#search").val("");
        $("#btn-clear").addClass('d-none');
        searching(null, 2, 0, 20);
    });
});

function load_more(start) {
    var data = get_data(null, 2);
    $.get("search", {
        key: $("#search").val(),
        status: '[' + data[0].toString() + ']',
        date: data[1],
        start: start,
        end: start + 20,
        needLength: 0
    }, function (data) {
        var str = '';
        data = JSON.parse(data);
        var arr = data['result'];
        for (var i = 0; i < arr.length; i++) {
            str += '<li class="list-group-item">\n' +
                '            <div class="row">\n' +
                '                <div class="col-4 col-md">' +
                arr[i][0];
            if (arr[i][1] === 'F')
                str += ' <span class="badge badge-info">Found</span>';
            else
                str += ' <span class="badge badge-warning">Lost</span>';
            str += '</div>\n' +
                '                <div class="col-4 col-md">' + arr[i][2] + '</div>\n' +
                '                <div class="col-4 col-md">' + arr[i][3] + '</div>\n' +
                '                <div class="col-md hide-sm">' + arr[i][4] + '</div>\n' +
                '                <div class="col">\n' +
                '                    <a href="/detail/' + arr[i][5] + '"><button class="btn btn-sm btn-secondary m-auto">View Detail</button></a>' +
                '                </div>\n' +
                '            </div>\n' +
                '        </li>';
        }
        $("#mainTable").append(str);
    });
}


function get_data(obj, type) {
    var data = [];
    if (type === 0) {
        $("#all-status, #all-found, #all-lost").removeClass('active');
        $(obj).addClass('active');
    }
    else if (type === 1) {
        $("#all-time, #last-week, #last-month").removeClass('active');
        $(obj).addClass('active');
    }

    // Lost / Found (Dropdown 1)
    if ($("#all-status").hasClass('active')) {
        data.push(['L', 'F']);
    }
    if ($("#all-lost").hasClass('active')) {
        data.push(['L'])
    }
    if ($("#all-found").hasClass('active')) {
        data.push(['F'])
    }

    // Time (Dropdown 3)
    if ($("#last-week").hasClass('active')) {
        data.push(0);
    }
    if ($("#last-month").hasClass('active')) {
        data.push(1);
    }
    if ($("#all-time").hasClass('active')) {
        data.push(2);
    }
    $(obj).addClass('active');
    return data;
}

function searching(obj, type, start, end) {
    var data = get_data(obj, type);
    $.get("search", {
        key: $("#search").val(),
        status: '[' + data[0].toString() + ']',
        date: data[1],
        start: start,
        end: end,
        needLength: 1
    }, function (data) {
        printHTML(data);
    });
}

function printHTML(data) {
    var str = '<li class="list-group-item bg-light">\n' +
        '            <div class="row">\n' +
        '                <div class="col-4 col-md font-weight-bold">Name</div>\n' +
        '                <div class="col-4 col-md font-weight-bold">Location</div>\n' +
        '                <div class="col-4 col-md font-weight-bold">Date</div>\n' +
        '                <div class="col-md font-weight-bold hide-sm">Poster</div>\n' +
        '                <div class="col font-weight-bold"></div>\n' +
        '            </div>\n' +
        '        </li>';
    data = JSON.parse(data);
    var arr = data['result'];
    $("#numOfResults").html(data['length']);
    for (var i = 0; i < arr.length; i++) {
        str += '<li class="list-group-item">\n' +
            '            <div class="row">\n' +
            '                <div class="col-4 col-md">' +
            arr[i][0];
        if (arr[i][1] === 'F')
            str += ' <span class="badge badge-info">Found</span>';
        else
            str += ' <span class="badge badge-warning">Lost</span>';
        str += '</div>\n' +
            '                <div class="col-4 col-md">' + arr[i][2] + '</div>\n' +
            '                <div class="col-4 col-md">' + arr[i][3] + '</div>\n' +
            '                <div class="col-md hide-sm">' + arr[i][4] + '</div>\n' +
            '                <div class="col">\n' +
            '                    <a href="/detail/' + arr[i][5] + '"><button class="btn btn-sm btn-secondary m-auto">View Detail</button></a>' +
            '                </div>\n' +
            '            </div>\n' +
            '        </li>';
    }
    $("#mainTable").html(str);
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