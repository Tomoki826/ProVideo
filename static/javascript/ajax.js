// 非同期通信で配信情報取得
$('.ajax_providers').on('inview', function(event, isInView) {
    if (isInView) {
        var jQuery_element = $(this);
        var values = jQuery_element.attr('value').split(',');
        if (values[0] == "unloaded") {
            $.ajax({
                url: '/load_provider',
                type: 'POST',
                datatype: 'JSON',
                data : {'id': values[1], 'data_type': values[2]}
            })
            //通信成功時の処理
            .done( function(data) {
                jQuery_element.attr('value', 'loaded,' + values[1] + ',' + values[2]);
                replaceProviderInfo(jQuery_element, data);
            })
            //通信失敗時の処理
            .fail( function() {
                jQuery_element.attr('value', 'loaded,' + values[1] + ',' + values[2]);
                jQuery_element.find('.subscription').children('.icons').replaceWith('<div class="icons"><div class="icon"><abbr title="通信エラー"><img class="none_provider" src="../static/images/disconnect_provider_image.png" alt="Error" oncontextmenu="return false;"/></abbr></div></div>');
                jQuery_element.find('.buy').children('.icons').replaceWith('<div class="icons"><div class="icon"><abbr title="通信エラー"><img class="none_provider" src="../static/images/disconnect_provider_image.png" alt="Error" oncontextmenu="return false;"/></abbr></div></div>');
                jQuery_element.find('.rental').children('.icons').replaceWith('<div class="icons"><div class="icon"><abbr title="通信エラー"><img class="none_provider" src="../static/images/disconnect_provider_image.png" alt="Error" oncontextmenu="return false;"/></abbr></div></div>');
            })
        }
    }
});

// 非同期通信で配信情報のHTMLを書き換え
function replaceProviderInfo(element, data) {
    // サブスクリプションを表示
    if ('flatrate' in data) {
        text = "";
        for (var i in data['flatrate']) {
            text += '<div class="icon"><a href="/trend?provider=' + data['flatrate'][i]['provider_id'] + '">';
            text += '<abbr title="' + data['flatrate'][i]['provider_name'] + '">';
            text += '<img src="' + data['flatrate'][i]['logo_path'] + '"' + ' alt="' + data['flatrate'][i]['provider_name'] + '"' + ' oncontextmenu="return false;">';
            text += '</abbr></a></div>';
        }
        element.find('.subscription').children('.icons').replaceWith('<div class="icons">' + text + "</div>");
    }
    else {
        element.find('.subscription').children('.icons').replaceWith('<div class="icons"><div class="icon"><abbr title="情報なし"><img class="none_provider" src="../static/images/unfound_provider.svg" alt="Not Found" oncontextmenu="return false;"/></abbr></div></div>');
    }
    // 購入を表示
    if ('buy' in data) {
        text = "";
        for (var i in data['buy']) {
            text += '<div class="icon"><a href="/trend?provider=' + data['buy'][i]['provider_id'] + '">';
            text += '<abbr title="' + data['buy'][i]['provider_name'] + '">';
            text += '<img src="' + data['buy'][i]['logo_path'] + '"' + ' alt="' + data['buy'][i]['provider_name'] + '"' + ' oncontextmenu="return false;">';
            text += '</abbr></a></div>';
        }
        element.find('.buy').children('.icons').replaceWith('<div class="icons">' + text + "</div>");
    }
    else {
        element.find('.buy').children('.icons').replaceWith('<div class="icons"><div class="icon"><abbr title="情報なし"><img class="none_provider" src="../static/images/unfound_provider.svg" alt="Not Found" oncontextmenu="return false;"/></abbr></div></div>');
    }
    // レンタルを表示
    if ('rent' in data) {
        text = "";
        for (var i in data['rent']) {
            text += '<div class="icon"><a href="/trend?provider=' + data['rent'][i]['provider_id'] + '">';
            text += '<abbr title="' + data['rent'][i]['provider_name'] + '">';
            text += '<img src="' + data['rent'][i]['logo_path'] + '"' + ' alt="' + data['rent'][i]['provider_name'] + '"' + ' oncontextmenu="return false;">';
            text += '</abbr></a></div>';
        }
        element.find('.rental').children('.icons').replaceWith('<div class="icons">' + text + "</div>");
    }
    else {
        element.find('.rental').children('.icons').replaceWith('<div class="icons"><div class="icon"><abbr title="情報なし"><img class="none_provider" src="../static/images/unfound_provider.svg" alt="Not Found" oncontextmenu="return false;"/></abbr></div></div>');
    }
}

// 非同期通信で日本語の人物名を取得
$(function() {
    $('.ajax_name').on('inview', function(event, isInView) {
        if (isInView) {
            var jQuery_element = $(this);
            var values = jQuery_element.attr('value').split(',');
            if (values[0] == "unloaded") {
                var original_name = values[2];
                $.ajax({
                    url: '/load_personal_name',
                    type: 'POST',
                    datatype: 'JSON',
                    data : {'id': values[1]},
                })
                // 通信成功時の処理
                .done( function(data) {
                    if (data != '') {
                        original_name = data;
                    }
                    jQuery_element.attr('value', 'loaded');
                })
                // 通信失敗時の処理
                .fail( function(data) {
                    // 一旦名前を表示する
                    jQuery_element.attr('value', 'loaded');
                })
                // 通信終了時の処理
                .always( function(data) {
                    jQuery_element.html(original_name);
                    jQuery_element.wrapInner('<abbr title="' + original_name + '">');
                })
            }
        }
    });
})