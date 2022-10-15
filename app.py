import os
import datetime

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from TMDB_api import TMDB

from os.path import join, dirname
from dotenv import load_dotenv


# アプリを構成開始
app = Flask(__name__)

# テンプレートを自動で読み込む
app.config["TEMPLATES_AUTO_RELOAD"] = True

# セッションをPCファイルに保管する (クッキーは使用しない)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///provideo.db")

# APIの環境変数が存在するか？
# (APIキーのテンプレート・取得方法は".env.sample"を参照)
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
api_key = os.environ.get("API_KEY")
if not api_key:
    raise RuntimeError("API_KEY not set")

@app.after_request
def after_request(response):
    # キャッシュしないように設定
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# 映画・ドラマを検索するページ
@app.route("/", methods=["GET"])
def index():
       return render_template("index.html")

# アカウントのログイン
@app.route("/login", methods=["GET", "POST"])
def login():

    # セッション情報を消去
    session.clear()

    # POSTメソッドでログイン
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # ユーザーネーム・パスワードが入力されているか
        fail_check = False
        if not username:
            fail_check = True
            flash("ユーザー名を入力してください", "failed")
        if not password:
            fail_check = True
            flash("パスワードを入力してください", "failed")
        if fail_check == True:
            return render_template("login.html")

        # データベースからユーザー情報取得
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        # ユーザーネームが存在し，パスワードが正しいかチェック
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
            flash("ユーザーネームまたはパスワードが正しくありません", "failed")
            return render_template("login.html")

        # ログインユーザーを記憶
        session["user_id"] = rows[0]["id"]

        # ホームページにリダイレクト
        flash("ログインしました","success")
        return redirect("/")

    # GETメソッドではログイン情報を表示する
    else:
        return render_template("login.html")

# アカウント作成
@app.route("/register", methods=["GET", "POST"])
def register():

    # ユーザーを登録する
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # ユーザーネーム・パスワードが入力されているか，二つのパスワードが一致するか
        fail_check = False
        if not username:
            fail_check = True
            flash("ユーザー名を入力してください", "failed")
        if not password or not confirmation:
            fail_check = True
            flash("パスワードを入力してください", "failed")
        elif password != confirmation:
            fail_check = True
            flash("入力した2つのパスワードが一致しません", "failed")
        elif len(password) < 8:
            fail_check = True
            flash("パスワードが8文字未満です", "failed")
        if fail_check == True:
            return render_template("register.html")

        # ユーザーネームをデータベースと照合する
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        # ユーザーがすでに存在するか
        if len(rows) != 0:
            flash("既に存在するユーザーIDです", "failed")
            return render_template("register.html")

        # パスワードのハッシュ値を生成
        password_hash = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)

        # ユーザーを新規作成
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, password_hash)

        # ログインページにリダイレクト
        flash("アカウントを新規作成しました","success")
        return render_template("login.html")

    # register画面を表示する
    else:
        return render_template("register.html")

# アカウントのログアウト
@app.route("/logout")
def logout():

    # セッションを削除
    session.clear()

    # ログインページを表示する
    flash("ログアウトしました","success")
    return render_template("index.html")

# 映画作品を検索する
@app.route("/send", methods=["POST"])
def search():
    keywords = request.form.get("search")
    return redirect(url_for('search_result', keywords = keywords, page = 1))

@app.route("/search", methods=["GET"])
def search_result():

    # 配信されている映画を検索
    keywords = request.args['keywords']
    page = int(request.args['page'])
    soup = TMDB(api_key).search_movies(keywords, page)

    # 映画が見つかったかチェック
    if 'errors' in soup:
        flash("映画が見つかりませんでした","failed")
        return redirect("/")
    elif soup['results'] == []:
        flash("映画が見つかりませんでした","failed")
        return redirect("/")
    elif soup['total_results'] == 0:
        flash("映画が見つかりませんでした","failed")
        return redirect("/")

    search_result = []
    movie_id_list = []
    text_length = []
    search_titles = soup['results']
    total_pages = soup['total_pages']
    total_results = soup['total_results']

    for item in search_titles:

        # 取得したデータを整理
        search_result, movie_id_list = database_search(item, search_result, movie_id_list)

        # お気に入りか否やかチェック
        if not session == {}:
            where_param = "(movie_id = " + " or movie_id = ".join(list(map(str, movie_id_list))) +")"
            favorite_list = [d.get('movie_id') for d in db.execute("SELECT movie_id FROM favorite WHERE user_id = ? and " + where_param, session['user_id'])]
            for item1 in favorite_list:
                if item1 in movie_id_list:
                    for item2 in search_result:
                        if item1 == item2['id']:
                            item2['favorite'] = True

    return render_template("search.html", keywords = keywords, session = session, page = page, data = search_result, total_pages = total_pages, total_results = total_results)


# お気に入りを登録
@app.route('/favorite_process', methods=["POST"])
def favorite_process():
    movie_id = request.form.get("movie_id")
    status   = request.form.get("status")
    if status == "unliked-heart":
        db.execute("INSERT INTO favorite (user_id, movie_id, datetime) VALUES (?, ?, ?)", session['user_id'], movie_id, datetime.datetime.now())
    elif status == "liked-heart":
        db.execute("DELETE FROM favorite WHERE user_id = ? and movie_id = ?", session['user_id'], movie_id)
    return ("nothing")


# マイページを表示
@app.route('/send_mypage', methods=["GET", "POST"])
def send_mypage():
    return redirect(url_for('mypage', page = 1))

@app.route('/mypage', methods=["GET"])
def mypage():

    # SQLからデータを取得
    page = int(request.args['page'])
    search_titles = db.execute("SELECT movie_id FROM favorite WHERE user_id = ? ORDER BY datetime DESC LIMIT 20 OFFSET ?", session['user_id'], (page - 1) * 20)
    username = db.execute("SELECT username FROM users WHERE id = ?", session['user_id'])[0]['username']

    search_result = []
    movie_id_list = []
    text_length = []
    total_results = db.execute("SELECT COUNT(movie_id) FROM favorite WHERE user_id = ?", session['user_id'])[0]['COUNT(movie_id)']
    total_pages = -(-total_results // 20) # (20で割った値を切り上げ)

    for i in range(len(search_titles)):
        item = TMDB(api_key).get_movie(search_titles[i]['movie_id'])

        # 取得したデータを整理
        search_result, movie_id_list = database_search(item, search_result, movie_id_list)

    return render_template("mypage.html", username = username, keywords = None, page = page, data = search_result, total_pages = total_pages, total_results = total_results)


# ログイン必要
@app.route('/need_login', methods=["GET", "POST"])
def need_login():
    flash("この機能を使うにはログインしてください","failed")
    return render_template("login.html")


# データベースを探索する
def database_search(item, search_result, movie_id_list):

    # いろんな値を取得
    id = item['id']
    title = item['title']
    pos_path = item['poster_path']
    bac_path = item['backdrop_path']
    popularity = item['popularity']

    # 劇場公開日を取得
    rel_date = ""
    if 'release_date' in item:
        rel_date = item['release_date']
    if not len(rel_date) == 10:
        rel_date = "不明"

    # 映画のあらすじを取得
    overview = item['overview']
    if overview == "":
        overview = "(日本語版のあらすじデータなし)"

    # 評価を取得
    vote_count = item['vote_count']
    vote_average = item['vote_average']

    # リストに辞書を追加
    search_result.append({'id': id, 'favorite': False, 'title': title, 'words': len(overview), 'rel_date': rel_date, 'pos_path': pos_path, 'bac_path': bac_path, 'overview': overview, 'popularity': popularity, 'vote_count': vote_count, 'vote_average': vote_average})
    movie_id_list.append(id)

    return search_result, movie_id_list


# プロバイダー情報を取得
@app.route('/load_information', methods=["POST"])
def load_information():
    movie_id = request.form.get("movie_id")
    provider_search = TMDB(api_key).get_movie_provider(movie_id)['results']
    if 'JP' in provider_search:
        prov_info = (provider_search['JP'])
    else:
        prov_info = {}

    return (prov_info)