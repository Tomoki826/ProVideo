from flask import request, render_template, redirect, url_for
from main import app, api_key
from main.models.config import SENSITIVE_SEARCH
from main.models.TMDB import TMDB
from main.models.enum import Search
from main.models.search_data import Search_Data
from main.models.kanji import Japanese_check
from main.models.json import JSON

# ホームページ
@app.route("/", methods=["GET"])
def index(search_type=int(Search.DISCOVER_MOVIE)):
       # 特集ページを取得
       feature = JSON('./main/static/JSON/feature.json').get_json()
       # 話題の映画を取得
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
       # 検索結果の整理
       data2 = Search_Data(soup2).search_arrange(Search.DISCOVER_TV, page)
       data2['max_page'] = 1
       data2['total_results'] = min(20, data2['total_results'])
       # 検索エラーチェック
       if 'errors' in soup2 or soup2['results'] == [] or soup2['total_results'] <= 0:
              return render_template("error.html")
       # 検索結果を表示
       return render_template("home.html", feature=feature, data=data, data2=data2)


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
       data = Search_Data(soup).search_arrange(search_type, page, keywords)
       return render_template("index.html", data=data, soup=soup, error=False)

# 特集ページを取得
@app.route("/feature/<string:path>", methods=["GET"])
def feature(path):
       # 特集ページを取得
       feature_data = []
       raw_data = JSON('./main/static/JSON/feature.json').get_json()
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
              match item['data_type']:
                     case "movie":
                            single_soup = match_work_id(item['id'],TMDB(api_key).search_movies(item['name'], 1)['results'])
                     case "tv":
                            single_soup = match_work_id(item['id'],TMDB(api_key).search_tvshows(item['name'], 1)['results'])
                     case "person":
                            single_soup = match_work_id(item['id'],TMDB(api_key).search_person(item['name'], 1, SENSITIVE_SEARCH)['results'])
                     case _:
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