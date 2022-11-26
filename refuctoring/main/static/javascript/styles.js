// 画像のリンク切れで代替の画像を表示
$('.poster img').on('error', function() {
    $(this).attr('src','../static/images/unfound_image.svg');
});
$('.products .videos img').on('error', function() {
    $(this).attr('src','../static/images/unfound_image.svg');
});

// データの種類に合わせて調節
$('.description .name .type').html( function(index, element) {
    if (element == "映画") {
        $(this).css('color', '#FFFFFF');
        $(this).css('background-color', '#F46262');
    }
    else if (element == "テレビ・配信番組") {
        $(this).css('color', '#FFFFFF');
        $(this).css('background-color', '#628BF4');
    }
    else if (element == "人物") {
        $(this).css('color', '#FFFFFF');
        $(this).css('background-color', '#4FB76C');
    }
    else if (element == "アダルト") {
        $(this).css('color', '#FFFFFF');
        $(this).css('background-color', '#F471E7');
    }
    console.log(element);
})

// 非同期通信で配信情報取得
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