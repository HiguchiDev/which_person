$(function () {

    $(".voting_btn").on('click', function () {

        const this_ = $(this);
        const likeUrl = this_.attr("data-href"); // ユーザーのステータス情報
        const choice_num = this_.attr("data-choice_num"); // ユーザーのステータス情報

        $.ajax({
            headers: {
                'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content')
            },//Headersを書き忘れるとエラーになる
            url: likeUrl,
            type: "GET",

        })
            // Ajaxリクエスト成功時の処理
            .done(function (data) {
                ajaxReloadVoteQtyByChoiceNum(choice_num);

                if (data.processing_success) {
                    pickupChoice(choice_num);
                    inactiveButton();
                    activeCommentPostButton();
                    if (data.voted) {
                        //document.getElementById("voted_message").innerHTML = "投票完了"
                    } else {
                        //document.getElementById("voted_message").innerHTML = "既にこのお題には投票済みです。"
                    }
                }
            })
            // Ajaxリクエスト失敗時の処理
            .fail(function (data) {
                alert('投票に失敗しました。');
            })
    });
});

function pickupChoice(choice_num) {

    $('#choice_' + choice_num).animate({
        borderColor: "#05AF69",
    }, 1000);
}

function unPickupChoice(choice_num) {

    var defaultColor = $('body').css('backgroundColor')
    // 徐々に色が変化

    // 徐々に色が変化
    $('#choice_' + choice_num).animate({
        borderColor: defaultColor,
    }, 1000);
}

function ajaxButtonInactive() {
    var theme_id = JSON.parse(document.getElementById('theme_id').textContent);

    $.ajax({
        headers: {
            'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content')
        },//Headersを書き忘れるとエラーになる
        url: "/which_person/which/can_voting/" + theme_id,
        type: "GET",
        cache: false
    })
        // Ajaxリクエスト成功時の処理
        .done(function (data) {
            if (data.processing_success && !data.canVote) {
                inactiveButton();
                activeCommentPostButton();
                pickupChoice(data.choice_num);

            }
        })
        // Ajaxリクエスト失敗時の処理
        .fail(function (data) {

        })
}

function activeCommentPostButton() {
    $('#comment_post_button').fadeIn();
}

function inactiveCommentPostButton() {
    $('#comment_post_button').fadeOut();
}

function inactiveButton() {
    var voting_button_collection = document.getElementsByClassName('voting_btn');

    for (var i = 0; i < voting_button_collection.length; i++) {
        voting_button_collection[i].disabled = true;
    }

    $('#vote_cancel_button').fadeIn();
}

function activeVoteButton() {
    var voting_button_collection = document.getElementsByClassName('voting_btn');

    for (var i = 0; i < voting_button_collection.length; i++) {
        voting_button_collection[i].disabled = false;
    }

    $('#vote_cancel_button').fadeOut();
}

