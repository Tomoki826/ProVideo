// 画像のリンク切れで代替の画像を表示
$('.poster img').on('error', function() {
    $(this).attr('src','../static/images/unfound_image.svg');
});
$('.products .videos img').on('error', function() {
    $(this).attr('src','../static/images/unfound_image.svg');
});

// 作品画像をクリックして検索する
$('.videos-btn').on('click', function() {
    var query = {
        "page": "1",
        "keywords": $(this).attr('value'),
        "search_type": "3",
    };
    window.location.href = "/search?" + $.param(query);
})