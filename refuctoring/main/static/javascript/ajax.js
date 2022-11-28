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
        }
    }
});

// 非同期通信で配信情報のHTMLを書き換え
function replaceProviderInfo(element, data) {
    // サブスクリプションを表示
    if ('flatrate' in data) {
        text = "";
        for (var i in data['flatrate']) {
            text += '<abbr title="' + data['flatrate'][i]['provider_name'] + '">';
            text += '<img src="https://www.themoviedb.org/t/p/w300' + data['flatrate'][i]['logo_path'] + '"' + ' alt="' + data['flatrate'][i]['provider_name'] + '"' + ' oncontextmenu="return false;">';
            text += '</abbr>';
        }
        element.find('.subscription').children('.icons').replaceWith('<div class="icons">' + text + "</div>");
    }
    else {
        element.find('.subscription').children('.icons').replaceWith('<div class="icons"><abbr title="情報なし"><img src="../static/images/unfound_provider.svg" alt="Not Found"/></abbr></div>');
    }
    // 購入を表示
    if ('buy' in data) {
        text = "";
        for (var i in data['buy']) {
            text += '<abbr title="' + data['buy'][i]['provider_name'] + '">';
            text += '<img src="https://www.themoviedb.org/t/p/w300' + data['buy'][i]['logo_path'] + '"' + ' alt="' + data['buy'][i]['provider_name'] + '"' + ' oncontextmenu="return false;">';
            text += '</abbr>';
        }
        element.find('.rental').children('.icons').replaceWith('<div class="icons">' + text + "</div>");
    }
    else {
        element.find('.rental').children('.icons').replaceWith('<div class="icons"><abbr title="情報なし"><img src="../static/images/unfound_provider.svg" alt="Not Found"/></abbr></div>');
    }
    // レンタルを表示
    if ('rent' in data) {
        text = "";
        for (var i in data['rent']) {
            text += '<abbr title="' + data['rent'][i]['provider_name'] + '">';
            text += '<img src="https://www.themoviedb.org/t/p/w300' + data['rent'][i]['logo_path'] + '"' + ' alt="' + data['rent'][i]['provider_name'] + '"' + ' oncontextmenu="return false;">';
            text += '</abbr>';
        }
        element.find('.buy').children('.icons').replaceWith('<div class="icons">' + text + "</div>");
    }
    else {
        element.find('.buy').children('.icons').replaceWith('<div class="icons"><abbr title="情報なし"><img src="../static/images/unfound_provider.svg" alt="Not Found"/></abbr></div>');
    }
    // 読み込み完了後 スライドインする
    element.find('img').css('animation', 'fadein-right 0.5s ease-out forwards');
    setTimeout(function(){element.find('img').css('animation', '')}, 500);
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
                    // 読み込み完了後 スライドインする
                    jQuery_element.css('animation', 'fadein-right 0.5s ease-out forwards');
                })
                // 通信終了時の処理
                .always( function(data) {
                    jQuery_element.html(original_name);
                })
            }
        }
    });
})