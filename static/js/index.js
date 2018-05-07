$(document).ready(function () {
    $("#read").click(function () {
        $("#new").addClass('d-none');
    });
    $("#clear").click(function () {
        $("#search").val("");
        searching($("#search"), 3);
        $("#icon").removeClass("fa-times").addClass("fa-search");
    });
});

function changeIcon(obj) {
    searching(obj, 3);
    if ($("#search").val().length > 0)
        $("#icon").removeClass("fa-search").addClass("fa-times");
    else
        $("#icon").removeClass("fa-times").addClass("fa-search");

}

function get_data(obj, type) {
    var data = [];
    for (var i = 3; i < 6; i++) {
        if ($('.dropdown-item')[i].className.indexOf("active") > 0) {
            if ($(obj).html() !== $('.dropdown-item')[i].innerHTML && type === 0) {
                $('.dropdown-item')[i].className = "dropdown-item";
                continue;
            }
            if ($('.dropdown-item')[i].innerHTML === 'All') {
                data.push(['L', 'F']);
            }
            else {
                if ($('.dropdown-item')[i].innerHTML === 'Lost')
                    data.push(['L']);
                else
                    data.push(['F']);
            }
        }
    }
    for (i = 11; i < 14; i++) {
        if ($('.dropdown-item')[i].className.indexOf("active") > 0) {
            if ($(obj).html() !== $('.dropdown-item')[i].innerHTML && type === 1) {
                $('.dropdown-item')[i].className = "dropdown-item";
                continue;
            }
            if ($('.dropdown-item')[i].innerHTML === 'Last Week') {
                data.push(0);
            }
            else if ($('.dropdown-item')[i].innerHTML === 'Last Month') {
                data.push(1);
            }
            else {
                data.push(2);
            }
        }
    }
    var checked = [];
    for (i = 0; i < 5; i++) {
        if ($(".locations")[i].checked) {
            checked.push($(".locations")[i].value)
        }
    }
    data.push(checked);
    return data;
}

function searching(obj, type) {
    if (obj.tagName === 'A')
        $(obj).addClass("active");
    var data = get_data(obj, type);
    $.get("search", {
        key: $("#search").val(),
        status: '[' + data[0].toString() + ']',
        date: data[1],
        location: '[' + data[2].toString() + ']'
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
    if (data === ']') {
        $("#numOfResults").html(0);
        $("#mainTable").html(str);
        return;
    }
    var arr = eval(data);
    $("#numOfResults").html(arr.length);
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
            '                <div class="col mt-1">\n' +
            '                    <button class="btn btn-sm btn-secondary m-auto" onclick="show_detail(' + arr[i][5] + ')">View Detail</button>\n' +
            '                </div>\n' +
            '            </div>\n' +
            '        </li>';
    }
    $("#mainTable").html(str);
}

function show_detail(num) {
    console.log("/detail/" + num + "/");
    window.location.href = "/detail/" + num + "/";
}