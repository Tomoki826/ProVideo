// localStorage関係の処理
$(document).ready(function() {

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

  // オンオフボタンの初期色の設定
  $(".switch_label").each(function(index, element) {
    var $switch = $(this);
    var key = $switch.attr("value");
    if (getSingleData(key)) {
      $switch.removeClass("off");
      $switch.addClass("on");
    }
    else {
      $switch.removeClass("on");
      $switch.addClass("off");
    }
    $(element).css("visibility", "initial");
  });

  // オンオフボタンのクリック
  $(".switch_label span").on('click', function(){
    clickSingleButton(this);

    var ori_key = $(this).parent().attr("value");
    if (ori_key === "overview") {
      $(".description").each(function(index, element){displayInfo(element)});
    }

    $(".switch_label").each(function(index, element){
      var $switch = $(element);
      var key = $switch.attr("value");
      if (ori_key === key) {
        if (getSingleData(key)) {
          $switch.removeClass("off");
          $switch.addClass("on");
        }
        else {
          $switch.removeClass("on");
          $switch.addClass("off");
        }
      }
    });
  });

  // あらすじ・映画情報表示の切り替え
  $(".description").each(function(index, element){displayInfo(element)});

});

// ボタン情報の切り替え
function clickSingleButton(element) {
    var $switch = $(element).parent();
    var key = $switch.attr("value");
    if ($switch.hasClass("on")) {
      setSingleData(key, false);
    }
    else if ($switch.hasClass("off")) {
      setSingleData(key, true);
    }
};

// あらすじ・映画情報表示の切り替え
function displayInfo(element) {
  $overview = $(element).find(".overview");
  $provider = $(element).find(".ajax_providers");
  if (getSingleData("overview")) {
    $overview.css("display", "inherit");
    $provider.css("display", "none");
  }
  else {
    $overview.css("display", "none");
    $provider.css("display", "inherit");
  }
}

// クリックごとにCSSを設定する
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
    $(element).find(".heart-icon img").css('filter', '');
    $(element).find(".heading").css('color', '#FFFFFF');
  }
  else if (values[0] === "unliked") {
      $(element).find(".heart-icon img").css('filter', 'grayscale(100%) brightness(230%)');
      $(element).find(".heading").css('color', '#E1E1E1');
  }
}

// 一つのデータを追加・上書き
function setSingleData(key, value) {
  localStorage.setItem(key, JSON.stringify(value));
}

// 一つのデータを取得
function getSingleData(key) {
  return JSON.parse(localStorage.getItem(key));
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
