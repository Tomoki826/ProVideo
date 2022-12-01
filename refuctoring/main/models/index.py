from flask import request, render_template, redirect, url_for
from main import app, api_key
from main.models.config import SENSITIVE_SEARCH
from main.models.TMDB import TMDB
from main.models.enum import Search
from main.models.search_data import Search_Data
from main.models.kanji import Japanese_check

# ホームページ
@app.route("/", methods=["GET"])
def index(search_type=int(Search.DISCOVER_MOVIE)):
       # 話題の映画を取得
       page = 1
       soup = TMDB(api_key).discover_movie(page)
       # 検索結果の整理
       data = soup
       data = Search_Data(Search.DISCOVER_MOVIE, page, data).arrange()
       data['max_page'] = 1
       data['total_results'] = min(20, data['total_results'])
       # 検索エラーチェック
       if 'errors' in soup or soup['results'] == [] or soup['total_results'] <= 0:
              return render_template("error.html")
       # 話題のテレビ・配信番組を取得
       page = 1
       soup2 = TMDB(api_key).discover_tvshows(page)
       # 検索結果の整理
       data2 = soup2
       data2 = Search_Data(Search.DISCOVER_TV, page, data2).arrange()
       data2['max_page'] = 1
       data2['total_results'] = min(20, data2['total_results'])
       # 検索エラーチェック
       if 'errors' in soup2 or soup2['results'] == [] or soup2['total_results'] <= 0:
              return render_template("error.html")
       # 検索結果を表示
       return render_template("home.html", data=data, data2=data2, soup=soup)


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
       match search_type:
              case Search.MOVIES:
                     soup = TMDB(api_key).search_movies(keywords, page)
              case Search.TVSHOWS:
                     soup = TMDB(api_key).search_tvshows(keywords, page)
              case Search.PERSON:
                     soup = TMDB(api_key).search_person(keywords, page, SENSITIVE_SEARCH)
              case Search.MULTI:
                     soup = TMDB(api_key).search_multi(keywords, page, SENSITIVE_SEARCH)
       # 検索結果の整理
       data = soup
       data = Search_Data(search_type, page, data, keywords).arrange()
       return render_template("index.html", data=data, soup=soup, error=False)

# 特集ページを取得
@app.route("/feature", methods=["GET"])
def feature():
       pass

# お気に入り情報を取得
@app.route('/favorite', methods=["GET"])
def favorite():
       pass

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