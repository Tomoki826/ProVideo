from flask import Flask, request, render_template, redirect, url_for
from models.config import SENSITIVE_SEARCH
from models.TMDB import TMDB
from models.enum import Search
from models.kanji import Japanese_check
from models.json import JSON
from models.search_data import Search_Data

# Flask構成開始
app = Flask(__name__)

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
"""
トレンド機能は
映画、配信、人物のどれかで話題の20作品を表示する
?media=があれば、それを
無ければLocalStorageから、最後に呼び出したデータタイプを表示する
"""
@app.route("/", methods=["GET"])
def index():
       
       # クエリパラメータを取得
       print(request.args)

       # 特集ページを取得
       feature = JSON('./static/JSON/feature.json').get_json()
       # 話題の映画・配信番組・人物を取得
       page = 1
       soup = TMDB(api_key).discover_movie(page)
       # 検索結果の整理
       data = Search_Data(soup).search_arrange(Search.DISCOVER_MOVIE, page)
       data['max_page'] = 1
       data['total_results'] = min(20, data['total_results'])
       # 検索エラーチェック
       if 'errors' in soup or soup['results'] == [] or soup['total_results'] <= 0:
              return render_template("error.html")
       # 話題のテレビ・配信番組を取得
       page = 1
       soup2 = TMDB(api_key).discover_tvshows(page)
       return render_template("homepage.html", feature=feature, data=data)


# 作品を検索
@app.route("/search", methods=["GET"])
def search():
       # パラメータチェック
       if 'keywords' in request.args:
              keywords = request.args['keywords']
              if len(keywords) == 0: keywords = ' '
       else:
              return render_template("error.html")
       if 'page' in request.args:
              page = int(request.args['page'])
              if page <= 0: page = 1
       else:
              page = 1
       if 'search_type' in request.args:
              search_type = int(request.args['search_type'])
              if not (1 <= search_type and search_type <= 4):
                     return render_template("error.html")
       else:
              search_type = Search.MULTI
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
              if item['data_type'] == "movie":
                     single_soup = match_work_id(item['id'],TMDB(api_key).search_movies(item['name'], 1)['results'])
              elif item['data_type'] == "tv":
                     single_soup = match_work_id(item['id'],TMDB(api_key).search_tvshows(item['name'], 1)['results'])
              elif item['data_type'] == "person":
                     single_soup = match_work_id(item['id'],TMDB(api_key).search_person(item['name'], 1, SENSITIVE_SEARCH)['results'])
              else:
                     single_soup = item
              # データタイプを代入
              single_soup['media_type'] = item['data_type']
              soup['results'].append(single_soup)
       # コンテンツをフォーマット
       data["containers"] = Search_Data(soup).search_arrange()
       return render_template("feature.html", data=data)


# idと一致する検索結果を探す
def match_work_id(id, soup):
       for item in soup:
              if item['id'] == id:
                     return item
       return {}


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
@app.route('/favorite', methods=["GET"])
def favorite():
       pass


if __name__=='__main__':
       # デバッグ用
       app.run(debug=True, host='0.0.0.0')
       #app.run()