$(function () {

    $("#vote_cancel_button").on('click', function () {

        var theme_id = JSON.parse(document.getElementById('theme_id').textContent);

        $.ajax({
            headers: {
                'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content')
            },//Headersを書き忘れるとエラーになる
            url: "/which_person/which/vote_cancel/" + theme_id,
            type: "GET",

        })
            // Ajaxリクエスト成功時の処理
            .done(function (data) {
                if (data.processing_success && data.isCanceled) {
                    ajaxReloadVoteQtyByChoiceNum(data.canceledChoiceNum);
                    unPickupChoice(data.canceledChoiceNum);
                    activeVoteButton();
                    inactiveCommentPostButton();
                    //document.getElementById("voted_message").innerHTML = "取り消しました。";
                }
            })
            // Ajaxリクエスト失敗時の処理
            .fail(function (data) {
                alert('取り消しに失敗しました。');
            })
    });
});