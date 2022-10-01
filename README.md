# CS50 Final Project **Provideo**

## 概要
- プロジェクトタイトル: Provideo
- デモ映像: https://youtu.be/BhiZ4Ol6Vwk
- 開発者: @Tomoki826 ([Github](https://github.com/Tomoki826)) @Tomoki_826 ([Twitter](https://twitter.com/Tomoki_826))
- 居住地: 日本 愛知県名古屋市

2020年から家での映画鑑賞が増えてきており、気になってた映画が配信されていなくて困った事はありませんか？ "Provideo"はこのような自分自身の経験を元に制作しました。

このアプリを一言で表すと「映画の配信サービスを横断検索するウェブアプリ」

有名な映像検索サービスの"[TMDB](https://www.themoviedb.org/)"や"[JustWatch](https://www.justwatch.com/)"のAPIを使用しており、それらよりもシンプルなUIで、気になる映画を検索・ブックマークすることが可能になり大変便利です。

著作権の問題もクリアしています。表示される映画ポスターや配信サービスのロゴアイコンは、ローカルではなくAPIからクラウド上で取得しているので、TMDBの利用規約[1]に順守しており合法です。

## 使用言語
- Python
- HTML
- CSS
- Flask
- SQlite
- JavaScript
- JQuery

# **操作方法**

## 検索 /
フォームにキーワードを入力して「検索」ボタンで送信することで、GETメソッドで部分合致する映画を一覧表示します。

## 検索結果 /search
検索結果を20件ごとに表示します。日本国内でオンデマンド視聴可能な映画である場合、配信サービスのロゴを種類別「サブスクリプション/レンタル/購入」に分けて一覧表示します。気になった映画は「お気に入り」ボタンを押すことで非同期通信(Ajax)を介してSQliteにブックマークされます。ブックマークした映画はマイページから参照可能です。

## マイページ /mypage
「お気に入り」にした映画を20件ごとに表示します。検索結果と同じUIで配信情報も参照できます。ピンク色のハートマークを再度押すことで簡単にお気に入り解除ができます。

## ログイン・新規登録 /login・/register
アカウントをログインすることで「お気に入り」機能が利用可能になります。新規登録されたアカウントはSQliteに保存されて、パスワードはハッシュ化されるのでセキュリティ的に安全です。

## ログアウト /logout
セッションでログイン状態を記憶し続けると別のユーザーが乗っ取ってしまうリスクがあるので、使い終わったらログアウトは忘れずに行いましょう。

# **ファイル・フォルダ構成**

## app.py
webアプリケーションのベースとなるpython形式のファイルです。FlaskやAjaxによるルートに対する動作を規定しています。

## TMDB_api.py
pythonの関数ごとに詳細なクエリ文字列を設定して、TMDBのAPIを用いた映画情報の取得が可能になります。キーワードで検索する際は、`TMDB().search_movies()`メソッドでキーワード・ページ数のカラムを格納して、`TMDB()._json_by_get_request()`でURLを生成します。配信サービス情報の取得は`TMDB().get_movie_provider()`で行えます。

## .env, .env.sample
エクスプローラー上には非表示のファイルであり、TMDBから取得したAPIキーを`.env.sample`の形式に従って`.env`に記入する必要があります。APIキーの取得方法は[こちら](https://kb.synology.com/ja-jp/DSM/tutorial/How_to_apply_for_a_personal_API_key_to_get_video_info#:~:text=The%20Movie%20Database%20%E3%82%A6%E3%82%A7%E3%83%96%E3%82%B5%E3%82%A4%E3%83%88%E3%81%AB%E3%82%B5%E3%82%A4%E3%83%B3%E3%82%A4%E3%83%B3%E3%81%99%E3%82%8B%E3%81%8B%E3%80%81%E3%81%82%E3%82%8B%E3%81%84%E3%81%AF%E3%82%A2%E3%82%AB%E3%82%A6%E3%83%B3%E3%83%88%E3%82%92%E4%BD%9C%E6%88%90%E3%81%97%E3%81%A6%E3%81%8F%E3%81%A0%E3%81%95%E3%81%84%E3%80%82%20%E3%82%A2%E3%82%AB%E3%82%A6%E3%83%B3%E3%83%88%20%E3%82%A2%E3%82%A4%E3%82%B3%E3%83%B3%E3%81%AE%E4%B8%8B%E3%81%A7,%5B%E8%A8%AD%E5%AE%9A%5D%20%E3%82%92%E3%82%AF%E3%83%AA%E3%83%83%E3%82%AF%E3%81%97%E3%81%BE%E3%81%99%E3%80%82%20API%20%E3%83%9A%E3%83%BC%E3%82%B8%E3%81%A7%E3%80%81%20%5BAPI%20%E3%82%AD%E3%83%BC%E3%82%92%E3%83%AA%E3%82%AF%E3%82%A8%E3%82%B9%E3%83%88%5D%20%E3%82%92%E3%82%BB%E3%82%AF%E3%82%B7%E3%83%A7%E3%83%B3%E3%81%AE%E4%B8%8B%E3%81%A7%E3%83%AA%E3%83%B3%E3%82%AF%E3%82%92%E3%82%AF%E3%83%AA%E3%83%83%E3%82%AF%E3%81%97%E3%81%BE%E3%81%99%E3%80%82)。

## provideo.db
アプリケーションに組み込まれたSQLiteデータベースでアカウント情報やお気に入りにした映画情報を記録しています。テーブルは「`favorite`」「`users`」の二つで、各テーブルにはユーザーID(`user_id`)やパスワードのハッシュ値(`hash`)、お気に入りにした映画ID(`movie_id`)などをカラムとして格納しています。

## /templates
画面表示に必須なHTMLファイルは全てこのディレクトリに保存されております。Flaskのフレームワークを使用しており、pythonの条件分岐による動的なwebページの表示が可能です。このディレクトリ中の全ファイルは下記の通りです。
- `index.html` [2]
- `layout.html`
- `login.html` [3]
- `mypage.html` [4]
- `page.html`
- `register.html` [5]
- `search_form.html`
- `search.html` [6]

## /static
webページのアイコンや背景などの著作権フリーな画像素材や CSS・JavaScriptの静的ファイルは全てこのディレクトリに保存されております。JavaScriptはJQueryのライブラリを採用することで、ページのリロード不要でAjaxによるお気に入り状態の更新が可能になります。このディレクトリ中の全ファイルは下記の通りです。
- `jquery.inview.min.js` [7]
- `material_background_image.jpg` [8]
- `material_favorite.png` [9]
- `material_kachinko.png` [9]
- `material_noimage.png` [9]
- `material_preloader.gif` [10]
- `styles.css`
- `styles.js`

## /flask_session
前述の通りFlaskはアプリケーションに組み込まれているため、セッション情報はこのディレクトリに保存されます。

___

### 脚注

1. [API Terms of Use — The Movie Database (TMDB)](https://www.themoviedb.org/documentation/api/terms-of-use)
2. 検索ページ(/)を表示
3. ログインページ(/login)を表示
4. マイページ(/mypage)を表示
5. 新規登録ページ(/register)を表示
6. 検索結果ページ(/search)を表示
7. [JavaScript 'inview' Plugin](https://github.com/protonet/jquery.inview)
8. [劇場の赤い座席の列](https://jp.freepik.com/free-photo/rows-of-red-seats-in-a-theater_3532061.htm#query=cinema&position=11&from_view=keyword)
9. [かわいいフリー素材集 いらすとや](https://www.irasutoya.com/)
10. [Pixelbuddha FLAT PRELOADERS](https://pixelbuddha.net/animation/flat-preloaders)