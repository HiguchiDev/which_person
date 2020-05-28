$(function () {

    ajaxReloadVoteQty();    //既存投票数取得、表示
    ajaxButtonInactive();   //投票済みか判定し、ボタンの非活性化

});

function ajaxReloadVoteQty() {
    var theme_id = JSON.parse(document.getElementById('theme_id').textContent);

    $.ajax({
        headers: {
            'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content')
        },//Headersを書き忘れるとエラーになる
        url: "/which_person/which/vote_qty/" + theme_id,
        type: "GET",
        cache: false
    })
        // Ajaxリクエスト成功時の処理
        .done(function (data) {
            if (data.get_success) {
                $("#choice1_qty").fadeOut(function () {
                    document.getElementById("choice1_qty").innerHTML = data.choice1_qty;
                    $("#choice1_qty").fadeIn();
                });

                $("#choice2_qty").fadeOut(function () {
                    document.getElementById("choice2_qty").innerHTML = data.choice2_qty;
                    $("#choice2_qty").fadeIn();
                });
            }
        })
        // Ajaxリクエスト失敗時の処理
        .fail(function (data) {
            alert('投票数の取得に失敗しました。');
        })
}


function ajaxReloadVoteQtyByChoiceNum(choice_num) {
    var theme_id = JSON.parse(document.getElementById('theme_id').textContent);

    $.ajax({
        headers: {
            'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content')
        },//Headersを書き忘れるとエラーになる
        url: "/which_person/which/vote_qty/" + theme_id,
        type: "GET",
        cache: false
    })
        // Ajaxリクエスト成功時の処理
        .done(function (data) {
            if (data.get_success) {

                if (choice_num == 1) {
                    $("#choice1_qty").fadeOut(function () {
                        document.getElementById("choice1_qty").innerHTML = data.choice1_qty;
                        $("#choice1_qty").fadeIn();
                    });
                } else if (choice_num == 2) {
                    $("#choice2_qty").fadeOut(function () {
                        document.getElementById("choice2_qty").innerHTML = data.choice2_qty;
                        $("#choice2_qty").fadeIn();
                    });
                }
            }
        })
        // Ajaxリクエスト失敗時の処理
        .fail(function (data) {
            alert('投票数の取得に失敗しました。');
        })
}