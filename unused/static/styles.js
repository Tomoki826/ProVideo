// Ajaxでお気に入り更新
$(function() {
    $('#favorite-heart img').on('click', function() {
        var movie_id = element.parent().val();
        var status   = element.attr('class');
        if (status != "need-login") {
            $.ajax({
                url: '/favorite_process',
                type: 'post',
                datatype: 'JSON',
                data : {"movie_id": movie_id, "status": status},
            }).done(function(data){
                //通信成功時の処理
                element.toggleClass('liked-heart').toggleClass('unliked-heart');
            })
        } else {
            window.location.href = "/need_login";
        }
    })
})

// ホバーで配信情報を表示
$(function() {
    $("[id^='load-point']").on('inview', function(event, isInView) {
        if (isInView) {
            var element  = $(this);
            var movie_id = element.attr('id').slice(11);
            var status   = element.attr('value');
            if (status == "unloaded") {
                $.ajax({
                    url: '/load_information',
                    type: 'post',
                    datatype: 'JSON',
                    data : {"movie_id": movie_id},
                }).done(function(data){
                    //通信成功時の処理
                    element.attr('value', 'loaded');
                    replaceHtml(element, data)
                })
            }
        }
    });
})

// HTMLを非同期通信で書き換える
function replaceHtml(element, data) {
key_length = Object.keys(data).length
if (key_length) {
    element.next().next().replaceWith('<tr class="replace3" style="height: 0; padding: 0; margin: 0;"><td colspan="2"></td></tr>');
    if ('flatrate' in data) {
        // サブスクリプションを表示
        string = '<td class="status-icon fadein-right" nowrap><span class="round-text">サブスクリプション</span></td><td>';
        for (var i in data['flatrate']) {
            string += '<img class="provider-image fadein-right" src="https://www.themoviedb.org/t/p/w300' + data['flatrate'][i]['logo_path'] + '"' + ' oncontextmenu="return false;">';
        }
        string += '</td>';
        element.find('.replace1').replaceWith(string);
        if ('buy' in data) {
            element.next().replaceWith('<tr><td class="provider-buttom-line" colspan="2"></td></tr>');
        }
    }
    if ('buy' in data) {
        // 購入を表示
        string = '<tr><td class="status-icon fadein-right" nowrap><span class="round-text">購入可能</span></td><td>';
        for (var i in data['buy']) {
            string += '<img class="provider-image fadein-right" src="https://www.themoviedb.org/t/p/w300' + data['buy'][i]['logo_path'] + '"' + ' oncontextmenu="return false;">';
        }
        string += '</td></tr>';
        element.next().next().replaceWith(string);
        if ('rent' in data) {
            element.next().next().next().replaceWith('<tr><td class="provider-buttom-line" colspan="2"></td></tr>');
        }
    }
    if ('rent' in data) {
        // レンタルを表示
        string = '<tr><td class="status-icon fadein-right" nowrap><span class="round-text">レンタル可能</span></td><td>';
        for (var i in data['rent']) {
            string += '<img class="provider-image fadein-right" src="https://www.themoviedb.org/t/p/w300' + data['rent'][i]['logo_path'] + '"' + ' oncontextmenu="return false;">';
        }
        string += '</td></tr>';
        element.next().next().next().next().replaceWith(string);
    }
    if (('flatrate' in data) && ('buy' in data == false) && ('rent' in data)) {
        element.next().next().replaceWith('<tr><td class="provider-buttom-line" colspan="2"></td></tr>');
    }
    string = '<tr><td class="link-info fadein-right" colspan="3"><a href="' + data['link'] + '" target="_blank" rel="noopener"><button class="btn" nowrap>配信情報はこちら</button></a>'
    element.next().next().next().next().next().replaceWith(string);
} else {
    element.next().next().replaceWith('<td class="status-icon fadein-right" nowrap colspan="2"><span class="round-text">オンデマンド配信なし</span></td>');
}

}

$(document).ready(function(){
    jQuery("#background-fade").delay(1000).fadeIn(1000);
});