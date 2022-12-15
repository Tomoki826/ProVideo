from flask import Flask, request, render_template, redirect, url_for, session
from models.config import SENSITIVE_SEARCH
from models.TMDB import TMDB
from models.enum import Search
from models.kanji import Japanese_check
from models.json import JSON
from models.search_data import Search_Data

# Flask構成開始
app = Flask(__name__)

# sessionの設定
app.secret_key = "user"

# 設定ファイル
app.config.from_object('models.config')

# APIの環境変数が存在するか？
# (APIキーのテンプレート・取得方法は".env.sample"を参照)
import os
from os.path import join, dirname
from dotenv import load_dotenv
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
api_key = os.environ.get("API_KEY")
if not api_key:
    raise RuntimeError("API_KEY not set")

# ホームページ
@app.route("/", methods=["GET"])
def index():

       # クエリパラメータを取得
       media_type = request.args.get('media')
       if media_type == None or media_type == "movie":
              soup = TMDB(api_key).discover_movie(1)
              data = Search_Data(soup).search_arrange(Search.DISCOVER_MOVIE, 1)
              discover_type = "映画"
              print_sort = "配信中 注目順"
       elif media_type == "tv":
              soup = TMDB(api_key).discover_tvshows(1)
              data = Search_Data(soup).search_arrange(Search.DISCOVER_TV, 1)
              discover_type = "テレビ・配信番組"
              print_sort = "配信中 注目順"
       elif media_type == "person":
              soup = TMDB(api_key).discover_person(1)
              data = Search_Data(soup).search_arrange(Search.DISCOVER_PERSON, 1)
              discover_type = "人物"
              print_sort = "注目順"
       else:
              return render_template("error.html")

       # 特集ページを取得
       feature = JSON('./static/JSON/feature.json').get_json()
       # 検索結果の整理
       data['max_page'] = 1
       data['total_results'] = min(20, data['total_results'])
       # 検索エラーチェック
       if 'errors' in soup or soup['results'] == [] or soup['total_results'] <= 0:
              return render_template("error.html")
       
       # レンダリング
       data['site_data'] = {
              'discover_type' : discover_type,
              'print_sort' : print_sort,
              'tab_data' : [
                     ["movie",  "/?media=movie#scroll",  "映画"],
                     ["tv",     "/?media=tv#scroll",     "テレビ・配信番組"],
                     ["person", "/?media=person#scroll", "人物"]
              ]
       }
       return render_template("homepage.html", feature=feature, data=data)


# 作品を検索
@app.route("/search", methods=["GET"])
def search():
       # パラメータチェック
       keywords = request.args.get('keywords', '')
       if keywords == '':
              return render_template("error.html")
       page = int(request.args.get('page', 1))
       if page <= 0 or page > 500:
              return render_template("error.html")
       search_type = int(request.args.get('search_type', Search.MULTI))
       if not (1 <= search_type and search_type <= 4):
              return render_template("error.html")
       # TMDBで検索する
       if search_type == Search.MOVIES:
              soup = TMDB(api_key).search_movies(keywords, page)
       elif search_type == Search.TVSHOWS:
              soup = TMDB(api_key).search_tvshows(keywords, page)
       elif search_type == Search.PERSON:
              soup = TMDB(api_key).search_person(keywords, page, SENSITIVE_SEARCH)
       elif search_type == Search.MULTI:
              soup = TMDB(api_key).search_multi(keywords, page, SENSITIVE_SEARCH)
       # 検索結果の整理
       data = Search_Data(soup).search_arrange(search_type, page, keywords)
       # レンダリング
       data['site_data'] = {
              'page_url': "/search",
              'page_tab_data' : [
                     ["keywords", data['keywords']],
                     ["search_type", data['search_type']],
              ],
       }
       return render_template("index.html", data=data, soup=soup, error=False)


# 特集ページを取得
@app.route("/feature/<string:path>", methods=["GET"])
def feature(path):
       # 特集ページを取得
       feature_data = []
       raw_data = JSON('./static/JSON/feature.json').get_json()
       for item in raw_data['feature']:
              if item['path'] == "/" + path:
                     feature_data = item['contents']
                     break
       else:
              return render_template("error.html")
       # ヘッダーデータを整理
       data = {
              "title": feature_data['title'],
              "title-font": feature_data['title-font'],
              "image": feature_data['image'],
              "color": feature_data['color'],
              "date": feature_data['date'],
              "writer": feature_data['writer'],
              "containers": {}
       }
       # コンテンツデータを整理
       soup = {'results': []}
       for item in feature_data['containers']:
              if item['media_type'] == "movie" or item['media_type'] == "tv" or item['media_type'] == "person":
                     single_soup = match_work_id(item['id'], item['name'], item['media_type'])
              else:
                     single_soup = item
              if single_soup != None:
                     soup['results'].append(single_soup)
       # コンテンツをフォーマット
       data["containers"] = Search_Data(soup).search_arrange()
       return render_template("feature.html", data=data)


# idと一致する検索結果を探す
def match_work_id(id, name, media_type="Unknown"):
       if media_type == "unknown" : return None
       page = 1
       while True:
              if media_type == "movie":
                     soup = TMDB(api_key).search_movies(name, page, SENSITIVE_SEARCH)
              elif media_type == "tv":
                     soup = TMDB(api_key).search_tvshows(name, page, SENSITIVE_SEARCH)
              elif media_type == "person":
                     soup = TMDB(api_key).search_person(name, page, SENSITIVE_SEARCH)
              if soup.get("results", []) == []: return None
              for item in soup["results"]:
                     if item['id'] == id:
                            item['media_type'] = media_type
                            return item
              page += 1


# プロバイダー情報を取得
@app.route('/load_provider', methods=["POST"])
def load_provider():
       id = request.form.get("id")
       data_type = request.form.get("data_type")
       if data_type == 'tv-sensitive': data_type = 'tv'
       provider_search = TMDB(api_key).get_provider_info(id, data_type)
       if 'results' in provider_search:
              data = provider_search['results'].get('JP', {})
       else:
              data = {}
       return data


# 日本語の人物名を取得
@app.route('/load_personal_name', methods=["POST"])
def load_personal_name():
       id = request.form.get("id")
       soup = TMDB(api_key).person_id(int(id))
       if 'also_known_as' in soup:
              return Japanese_check(soup['also_known_as'])
       else:
              return ''


# トレンド情報を取得
"""
トレンド機能は
配信業者一つ一つで話題の20作品を表示する
?provider=があれば、そのプロバイダーを
無ければLocalStorageから、最後に呼び出したプロバイダーを表示する
"""
@app.route('/trend', methods=["GET"])
def trend(provider):
       pass


# お気に入り情報を取得
# 映画・テレビ番組・人物を?media=で細分化する
# ?page=でページ指定可能
# LocalStorageとPython内の変数で同期？
@app.route('/favorite', methods=["GET"])
def favorite():
       # クエリパラメータを取得
       media_type = request.args.get('media', "movie")
       if media_type == "movie":
              data_type = "movie"
              print_type = "映画"
       elif media_type == "tv":
              data_type = "tv"
              print_type = "テレビ・配信番組"
       elif media_type == "person":
              data_type = "person"
              print_type = "人物"
       else:
              return render_template("error.html")
       page = int(request.args.get('page', 1))
       total_results = len(session['user'][data_type])
       if page <= 0:
              return render_template("error.html")
       elif page > (total_results - 1) // 20 + 1 and total_results >= 1:
              page = (total_results - 1) // 20 + 1
       # コンテンツデータを整理
       data = {}
       soup = {'results': []}
       for item in session['user'][data_type][(page - 1) * 20 : page * 20]:
              single_soup = match_work_id(int(item[0]), item[1], data_type)
              if single_soup != None:
                     soup['results'].append(single_soup)
       data = Search_Data(soup).search_arrange(Search.MULTI, page)
       # ページ数の調節
       data['total_results'] = total_results
       data['max_page'] = (total_results - 1) // 20 + 1
       # レンダリング
       data['site_data'] = {
              'page_url': "/favorite",
              'page_tab_data' : [["media", media_type]],
              'print_type' : print_type,
              'tab_data' : [
                     ["movie",  "/favorite?media=movie",  "映画"],
                     ["tv",     "/favorite?media=tv",     "テレビ・配信番組"],
                     ["person", "/favorite?media=person", "人物"]
              ]
       }
       return render_template("favorite.html", data=data)


# LocalStorageとFlaskのデータを同期(Cookieが必要)
@app.route('/sync_localstorage', methods=["POST"])
def sync_localstorage():
       session['user'] = {'movie': [], 'tv': [], 'person': []}
       session.permanent = True
       convert_localdata('movie', request.form)
       convert_localdata('tv', request.form)
       convert_localdata('person', request.form)
       return "OK"


# ローカルストレージのデータを扱いやすいように変換
def convert_localdata(key, post_data):
       tmp = 0
       while True:
              li = post_data.getlist(key + '[0]['+ str(tmp) +'][]')
              if li:
                     if (SENSITIVE_SEARCH or li[3] == 'false'):
                            session['user'][key].append(li)
              else:
                     return
              tmp += 1


if __name__=='__main__':
       # デバッグ用
       app.run(debug=True, host='0.0.0.0')
       #app.run()