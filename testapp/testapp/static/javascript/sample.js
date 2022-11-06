// ウィンドウ読み込み時にtestの要素を5秒後に赤くする
window.onload = function() {
    var changeColor = function() {
        var e = document.getElementById('test');
        e.style.color = 'red';
        console.log("書き換えテスト")
    }
    setTimeout(changeColor, 5000);
}