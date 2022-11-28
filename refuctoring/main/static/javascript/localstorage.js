// localStorage関係の処理
$(function() {

  // お気に入りの色を設定する
  $(".favorite").each(function(index, element) {
      var values = $(element).attr('value').split(',');
      var data = JSON.parse(localStorage.getItem(values[1]));
      var id = parseInt(values[2], 10);
      if (data !== null) {
        if (data.indexOf(id) !== -1) $(element).attr('value', "liked," + values[1] + "," + values[2]);
      }
      setHeartColor(element);
  });

  // お気に入りボタンのクリック
  $(".favorite").on('click', function(){
      var values = $(this).attr('value').split(',');
      if (values[0] === "unliked") {
        $(this).attr('value', "liked," + values[1] + "," + values[2]);
        setFavoriteData(values[1], parseInt(values[2], 10));
        setHeartColor(this);
        clickAnimation($(this).find(".heart-icon"), 'animation', "heart-click 0.25s 0s ease 1 normal backwards");
      }
      else if (values[0] === "liked") {
        $(this).attr('value', "unliked," + values[1] + "," + values[2]);
        delFavoriteData(values[1], parseInt(values[2], 10));
        setHeartColor(this);
        clickAnimation($(this).find(".heart-icon"), 'animation', "heart-click 0.25s 0s ease 1 normal backwards");
      }
  });
});

// クリックごとにCSSのアニメーション
function clickAnimation($element, key, value) {
  // アニメーションの設定
  $element.css(key, value);
  // コピーして古いものと置き換え
  var copied = $element.clone(true);
  $element.before(copied);
  $element.remove();
}

// お気に入りの色を設定する
function setHeartColor(element) {
  var values = $(element).attr('value').split(',');
  if (values[0] === "liked") {
      $(element).find(".heart-icon").css('fill', '#E32626');
      $(element).find(".heading").css('color', '#FFFFFF');
  }
  else if (values[0] === "unliked") {
      $(element).find(".heart-icon").css('fill', '#E1E1E1');
      $(element).find(".heading").css('color', '#E1E1E1');
  }
}

// 作品・人物情報を追加
function setFavoriteData(type, id) {
  var data = JSON.parse(localStorage.getItem(type));
  if (data === null) {
    data = [id];
  }
  else if (data.indexOf(id) === -1) {
    data.push(id);
  }
  localStorage.setItem(type, JSON.stringify(data));
}

// 作品・人物情報を削除
function delFavoriteData(type, id) {
  var data = JSON.parse(localStorage.getItem(type));
  if (data !== null) {
    var index = data.indexOf(id);
    if (index !== -1) data.splice(index, 1);
    localStorage.setItem(type, JSON.stringify(data));
  }
}
