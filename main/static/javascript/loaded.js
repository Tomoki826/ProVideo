// HTML読み込み完了直後に実行
$(document).ready(function() {

    // 文字数が多すぎたら省略する
    $(".description").each(function(index, element){
        // 作品名を調節
        var $title = $(element).find('.title');
        text_shorten($title, $title.children(), 360);
        $title.css("display","inherit");
        // ジャンルを調節
        var $genre = $(element).find('.genre');
        text_shorten($genre, $genre.children(), 360);
        $genre.css("display","inherit");
    });

    // あらすじの文字数が多すぎたら省略する
    var max_overview = 240;
    $(".overview").each(function(index, element){
        var $textbox = $(element).find(".text");
        var text = $textbox.html();
        if (text.length > max_overview) {
            $textbox.html(text.slice(0, max_overview) + "…");
        }
    });

    // お気に入りの色を設定する
    $(".favorite").each(function(index, element){
        var check = $(element).attr('value');
        if (check == "liked") {
            $(element).find(".heart-icon").css('fill', '#E32626');
            $(element).find(".heading").css('color', '#FFFFFF');
        }
    });

    // 作品・人物情報をDOMが完成した後に表示する
    $(".description").each(function(index, element){
        setTimeout(function(){$(element).css("visibility", "initial")}, 1);
    });
});

// テキストを短くする
function text_shorten($block_box, $inline_box, max_length) {
    if ($block_box.width() > max_length) {
        var text = $inline_box.html();
        $block_box.css('position', 'absolute');
        $inline_box.wrap('<abbr title="' + text + '">');
        $block_box.wrap('<div class="slide-box">');
        while ($block_box.width() > max_length) {
            text = text.slice(0, -1);
            $inline_box.html(text + "…");
        }
    }
}