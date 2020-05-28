$(function () {

    var theme_id = JSON.parse(document.getElementById('theme_id').textContent);

    $.ajax({
        url: "/which_person/which/comment_list/" + theme_id,
        method: "GET",
        timeout: 10000,
        dataType: "json",
        cache: false
    })
        .done(function (data) {

            if (!isEmpty(data)) {
                for (var item in data) {

                    output_comment_html(data[item]);
                }
            }

        })
        // Ajaxリクエスト失敗時の処理
        .fail(function (data) {
            console.log("コメント送信失敗")
        })

    $('.js-modal-open').on('click', function () {
        $('.js-modal').fadeIn();
        return false;
    });
    $('.js-modal-close').on('click', function () {
        $('.js-modal').fadeOut();
        document.comment_form.reset();
        return false;
    });


    $("#comment_form").submit(function (event) {
        event.preventDefault();

        var form = $(this);

        $.ajax({
            url: form.prop("action"),
            method: form.prop("method"),
            data: form.serialize(),
            timeout: 10000,
            dataType: "json",
        })
            .done(function (data) {
                output_comment_html(data);
                document.comment_form.reset();
                $('.js-modal').fadeOut();
            })
            // Ajaxリクエスト失敗時の処理
            .fail(function (data) {
                console.log("コメント送信失敗")
                alert("コメント送信に失敗しました。");
            })
    });
});

function isEmpty(obj) {
    for (let i in obj) {
        return false;
    }
    return true;
}

function output_comment_html(comment) {

    var comment_id = "comment_" + comment.id
    create_comment_div(comment_id)

    var csrf_token = document.getElementsByName("csrfmiddlewaretoken")[0];
    //console.log(csrf_token)

    var url = document.getElementById("comment_parts").textContent;
    $("#" + comment_id).load(url, function () {

        //コールバック後のjavascriptをここに記述
        document.getElementById("user_name").innerHTML = comment.user_name
        document.getElementById("user_name").id = "user_name_" + comment.id;
        var comment_html = comment.comment.replace(/\r?\n/g, '<br>')
        document.getElementById("comment_txt").innerHTML = comment_html
        document.getElementById("comment_txt").id = "comment_txt_" + comment.id;
        document.getElementById("csrf_token").value = csrf_token.value;
        document.getElementById("csrf_token").id = "csrf_token_" + comment.id;

        if (comment.choice_num == 1) {
            var backGroundColor = $('#choice_1').css('backgroundColor');
            $('#choice_color').css('backgroundColor', backGroundColor);

        } else if (comment.choice_num == 2) {
            var backGroundColor = $('#choice_2').css('backgroundColor');
            $('#choice_color').css('backgroundColor', backGroundColor);
        }

        document.getElementById("choice_color").id = "choice_color_" + comment.id;

        var user_id = JSON.parse(document.getElementById('user_id').textContent);

        if (user_id == comment.user_id) {
            document.getElementById("form_comment_id").value = comment.id;
            document.getElementById("form_comment_id").id = "form_comment_id_" + comment.id;
            create_comment_delete_form(comment_id);

        } else {
            document.getElementById("comment_delete_form").remove();
        }

    });

}

function create_comment_delete_form(comment_id) {

    var comment_del_url = document.getElementById("comment_delete_api").innerHTML
    var newCommentDeleteFormId = "comment_delete_form_" + comment_id;
    document.getElementById("comment_delete_form").id = newCommentDeleteFormId;
    document.getElementById(newCommentDeleteFormId).action = comment_del_url;

    $("#" + newCommentDeleteFormId).submit(function (event) {
        event.preventDefault();

        var form = $(this);

        $.ajax({
            url: form.prop("action"),
            method: form.prop("method"),
            data: form.serialize(),
            timeout: 10000,
            dataType: "json",
        })
            .done(function (data) {
                if (data.isCanceled) {
                    $("#comment_" + data.comment_id).fadeOut();
                    console.log("コメント削除成功 : " + data.comment_id)
                } else {
                    console.log("コメント削除失敗 : " + data.comment_id);
                }
            })
            // Ajaxリクエスト失敗時の処理
            .fail(function (data) {
                console.log("コメント削除失敗　通信エラー")
            })


    });

}

function create_comment_div(id) {

    var newElement = document.createElement("div");
    newElement.setAttribute("id", id);

    // 親要素（div）への参照を取得
    var parentDiv = document.getElementById("comment_message");
    // 追加
    parentDiv.insertBefore(newElement, parentDiv.firstChild);
}