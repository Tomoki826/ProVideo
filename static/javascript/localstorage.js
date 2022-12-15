// localStorage関係の処理
$(document).ready(function() {

  // お気に入りの色を設定する
  $(".favorite").each(function(index, element) {
      var values = $(element).attr('value').split(',');
      var data = JSON.parse(localStorage.getItem(values[1]));
      var id = parseInt(values[2], 10);
      if (data !== null) {
        for (var index in data) {
          if (id == data[index][0]) {
            $(element).attr('value', "liked," + values[1] + "," + values[2] + "," + values[3]);
            break;
          }
        }
      }
      setHeartColor(element);
  });

  // お気に入りボタンのクリック
  // values[1]: データタイプ
  // values[2]: 作品id
  // values[3]: 作品名
  $(".favorite").on('click', function(){
      var values = $(this).attr('value').split(',');
      if (values[0] === "unliked") {
        $(this).attr('value', "liked," + values[1] + "," + values[2] + "," + values[3] + "," + values[4]);
        setFavoriteData(values[1], parseInt(values[2], 10), values[3], parseBoolean(values[4]));
      }
      else if (values[0] === "liked") {
        $(this).attr('value', "unliked," + values[1] + "," + values[2] + "," + values[3] + "," + values[4]);
        delFavoriteData(values[1], parseInt(values[2], 10));
      }
      setHeartColor(this);
      clickAnimation($(this).find(".heart-icon"), 'animation', "heart-click 0.25s 0s ease 1 normal backwards");
      flask_local_sync();
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

  // AjaxでFlaskとLocalStorageを同期
  var webStorage = function () {
    if (sessionStorage.getItem('access')) {
      //2回目以降アクセス時の処理
      //console.log('2回目以降のアクセスです');
    } else {
      //初回アクセス時の処理
      sessionStorage.setItem('access', 0);
      //console.log('初回アクセスです');
      flask_local_sync();
    }
  }
  webStorage();

  // あらすじ・映画情報表示の切り替え
  $(".description").each(function(index, element){displayInfo(element)});

});

// 文字列型からBoolean型に変換
function parseBoolean(str) {
  // 文字列を判定
  return (str == 'true') ? true : false;
};

// AjaxでFlaskとLocalStorageを同期
function flask_local_sync() {
  $.ajax({
    url: '/sync_localstorage',
    type: 'POST',
    datatype: 'JSON',
    data : {
      "movie": [getSingleData("movie")],
         "tv": [getSingleData("tv")],
     "person": [getSingleData("person")]
    }
  })
};

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
function setFavoriteData(type, id, name, sensitive) {
  var currentDate = new Date();
  var data = JSON.parse(localStorage.getItem(type));
  if (data === null) {
    data = [[id, name, currentDate, sensitive]];
  }
  else if (data.indexOf(id) === -1) {
    data.unshift([id, name, currentDate, sensitive]);
  }
  localStorage.setItem(type, JSON.stringify(data));
}

// 作品・人物情報を削除
function delFavoriteData(type, id) {
  var data = JSON.parse(localStorage.getItem(type));
  if (data !== null) {
    for (var index in data) {
      if (id == data[index][0]) {
        data.splice(index, 1);
        break;
      }
    }
    localStorage.setItem(type, JSON.stringify(data));
  }
}

/*
// 要素をクリックしてLocalStorageをPOST送信
$('.localstorage_post').click(function() {
    data = {
       movie: getSingleData("movie"),
          tv: getSingleData("tv"),
      person: getSingleData("person")
    }
    form_post("/favorite", data)
});

// 架空のformでPOST送信
function form_post(path, params, method='post') {

  var form = document.createElement('form');
  form.method = method;
  form.action = path;

  for (var key in params) {
      if (params.hasOwnProperty(key)) {
          var hiddenField = document.createElement('input');
          hiddenField.type = 'hidden';
          hiddenField.name = key;
          hiddenField.value = params[key];
          form.appendChild(hiddenField);
      }
  }  
  document.body.appendChild(form);
  console.log(form);
  form.submit();
}
*/