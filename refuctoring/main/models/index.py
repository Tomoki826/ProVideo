from flask import request, render_template, redirect, url_for
from main import app, api_key
from main.models.TMDB import TMDB
from main.models.enum import Search
from main.models.search_data import Search_Data

# 成人向けを検索結果に含めるか？
sensitive_search = False

# ホームページ
@app.route("/", methods=["GET", "POST"])
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
                     soup = TMDB(api_key).search_person(keywords, page, sensitive_search)
              case Search.MULTI:
                     soup = TMDB(api_key).search_multi(keywords, page, sensitive_search)
              
       soup2 = TMDB(api_key).person_id(585211)
       # 検索結果の整理
       data = soup
       data = Search_Data(search_type, page, data, keywords).arrange()
       return render_template("index.html", data=data, soup=soup, soup2=soup2, error=False)