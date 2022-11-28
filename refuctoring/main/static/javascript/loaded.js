$(function() {
    // 文字数が多すぎたら省略する
    $(".description").each(function(index, element){
        // 作品名を調節
        var $title = $(element).find('.title');
        text_shorten($title, $title.children(), 360);
        // ジャンルを調節
        var $genre = $(element).find('.genre');
        text_shorten($genre, $genre.children(), 360);
    });

    // お気に入りの色を設定する
    $(".favorite").each(function(index, element){
        var check = $(element).attr('value');
        if (check == "liked") {
            $(element).find(".heart-icon").css('fill', '#E32626');
            $(element).find(".heading").css('color', '#FFFFFF');
        }
    });

    // お気に入りクリックを確認する
    $(".favorite").on('click', function(){
        var values = $(this).attr('value').split(',');
        console.log(values);
    });
});

// テキストを短くする
function text_shorten($block_box, $inline_box, max_length) {
    if ($inline_box.width() > max_length) {
        var text = $inline_box.html();
        $block_box.css('position', 'absolute');
        $inline_box.wrap('<abbr title="' + text + '">');
        $block_box.wrap('<div class="slide-box">');
        while ($inline_box.width() > max_length) {
            text = text.slice(0, -1);
            $inline_box.html(text + "…");
        }
    }
}