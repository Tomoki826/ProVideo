// 画像のリンク切れで代替の画像を表示
$('img').error(function() {
    $(this).attr('src','thumbnail.png');
});

// 非同期通信で配信情報取得
$(function() {
    $('.ajax_providers').on('inview', function(event, isInView) {
        if (isInView) {
            var element = $(this);
            var values = element.attr('value').split(',');
            if (values[0] == "unloaded") {
                $.ajax({
                    url: '/load_provider',
                    type: 'POST',
                    datatype: 'JSON',
                    data : {'id': values[1], 'data_type': values[2]},
                }).done(function(data) {
                    //通信成功時の処理
                    element.attr('value', 'loaded,' + values[1] + ',' + values[2]);
                    replaceProviderInfo(element, data);
                })
            }
        }
    });
})

// 非同期通信で配信情報のHTMLを書き換え
function replaceProviderInfo(element, data) {
    key_length = Object.keys(data).length;
    if (key_length > 0) {
        // サブスクリプションを表示
        if ('flatrate' in data) {
            text = "";
            for (var i in data['flatrate']) {
                text += '<img src="https://www.themoviedb.org/t/p/w300' + data['flatrate'][i]['logo_path'] + '"' + ' oncontextmenu="return false;">'
            }
            element.find('.subscription').children('.icons').replaceWith('<div class="icons">' + text + "</div>");
        }
        // 購入を表示
        if ('buy' in data) {
            text = "";
            for (var i in data['buy']) {
                text += '<img src="https://www.themoviedb.org/t/p/w300' + data['buy'][i]['logo_path'] + '"' + ' oncontextmenu="return false;">'
            }
            element.find('.subscription').children('.icons').replaceWith('<div class="icons">' + text + "</div>");
        }
        // レンタルを表示
        if ('rent' in data) {
            text = "";
            for (var i in data['rent']) {
                text += '<img src="https://www.themoviedb.org/t/p/w300' + data['rent'][i]['logo_path'] + '"' + ' oncontextmenu="return false;">'
            }
            element.find('.subscription').children('.icons').replaceWith('<div class="icons">' + text + "</div>");
        }
    }
    else {
    }
}

// 非同期通信で日本語の人物名を取得
$(function() {
    $('.ajax_name').on('inview', function(event, isInView) {
        if (isInView) {
            var element = $(this);
            var values = element.attr('value').split(',');
            if (values[0] == "unloaded") {
                $.ajax({
                    url: '/load_personal_name',
                    type: 'POST',
                    datatype: 'JSON',
                    data : {'id': values[1]},
                }).done(function(data) {
                    //通信成功時の処理
                    if (data != '') {
                        element.replaceWith('<div class="ajax_name" value="">' + data + '</div>');
                    }
                    element.attr('value', 'loaded,' + values[1]);
                })
            }
        }
    });
})