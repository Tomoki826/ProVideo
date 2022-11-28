// localStorage
$(function(){

  // localStorageへの書き込み関数
  function setLocalStorage(key, value) {
    localStorage.setItem(key, value);
  }
  
  // localStorageからの読み込み関数
  function getLocalStorage(key) {
    return localStorage.getItem(key);
  }

  // 初期表示時に前回保存された値を読み込んでセット
  $(".value-1").val(getLocalStorage("value-1"));

  // 保存ボタンクリック時の処理
  $(".save-btn").click(function(){
    setLocalStorage("value-1", $(".value-1").val());
    $(".status").text("ローカルストレージに保存しました");
  });
  
});