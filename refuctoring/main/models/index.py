from flask import request, render_template, redirect, url_for
from main import app, api_key
from main.models.TMDB import TMDB
from main.models.genre import Genre
from main.models.enum import Search
import datetime, re

# ホームページ
@app.route("/", methods=["GET", "POST"])
def index(search_type=Search.DISCOVER_MOVIE):
       if 'page' in request.args:
              page = int(request.args['page'])
       else:
              page = 1
       soup = TMDB(api_key).discover_movie(page)
       # 検索結果の整理
       data = soup
       data = result_arrangement(search_type, page, data)
       # 検索エラーチェック
       if 'errors' in soup or soup['results'] == [] or soup['total_results'] <= 0:
              return render_template("error.html")
       # 検索結果を表示
       return render_template("index.html", data=data, soup=soup)

# 作品を検索
@app.route("/search", methods=["GET"])
def search():
       # パラメータチェック
       if 'keywords' in request.args:
              keywords = request.args['keywords']
              print(len(keywords))
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
       if (search_type == Search.MOVIES):
              soup = TMDB(api_key).search_movies(keywords, page)
       elif (search_type == Search.TVSHOWS):
              soup = TMDB(api_key).search_tvshows(keywords, page)
       elif (search_type == Search.MULTI):
              soup = TMDB(api_key).search_multi(keywords, page)
       elif (search_type == Search.SENSITIVE):
              soup = TMDB(api_key).search_multi(keywords, page, True)
       # 検索結果の整理
       data = soup
       data = result_arrangement(search_type, page, data, keywords)
       # 検索エラーチェック
       #if 'errors' in soup or soup['results'] == [] or soup['total_results'] <= 0:
       #       return render_template("error.html")
       # 検索結果を表示
       return render_template("index.html", data=data, soup=soup, error=False)


# 検索情報をフォーマットする
def result_arrangement(search_type, page, in_data, keywords=''):
       data = {}
       data['keywords'] = keywords
       data['current_page'] = page
       data['max_page'] = (in_data['total_results'] - 1) // 20 + 1
       data['total_results'] = in_data['total_results']
       # 検索タイプ
       data['search_type'] = search_type
       if search_type == Search.MOVIES or search_type == Search.TVSHOWS or search_type == Search.MULTI or search_type == Search.SENSITIVE:
              data['search_type-btn'] = search_type
       else:
              data['search_type-btn'] = Search.MULTI
       # 検索データの整理
       data['results'] = []
       for item in in_data['results']:
              li_data = {}
              # 作品タイトル
              if 'adult' not in item:
                     li_data['adult'] = 'false'
              if 'title' in item:
                     li_data['title'] = item['title']
              elif 'name' in item:
                     li_data['title'] = item['name']
              elif 'original_name' in item:
                     li_data['title'] = item['original_name']
              else:
                     li_data['title'] = '(タイトル情報なし)'
              # 公開日
              if 'release_date' in item:
                     # 日付文字列の正規表現パターンと一致するか確認
                     if re.fullmatch(r'\d{4}-\d{2}-\d{2}', item['release_date']):
                            dte = datetime.datetime.strptime(item['release_date'], '%Y-%m-%d')
                            li_data['openday'] = '公開日: ' + str(dte.year) + '年' + str(dte.month) + '月' + str(dte.day) + '日'
              elif 'first_air_date' in item:
                     # 日付文字列の正規表現パターンと一致するか確認
                     if re.fullmatch(r'\d{4}-\d{2}-\d{2}', item['first_air_date']):
                            dte = datetime.datetime.strptime(item['first_air_date'], '%Y-%m-%d')
                            li_data['openday'] = '公開日: ' + str(dte.year) + '年' + str(dte.month) + '月' + str(dte.day) + '日'
              if 'openday' not in li_data:
                     li_data['openday'] = '公開日: 不明'
              # ジャンル
              if 'genre_ids' not in item or item.get('genre_ids') == []:
                     li_data['genre'] = 'ジャンル: 不明'
              else:
                     li_data['genre'] = 'ジャンル: '
                     for id in item['genre_ids']:
                             li_data['genre'] += Genre().name_get(id) + ' '
                     li_data['genre'] = li_data['genre'][:-1]
              # ポスター画像
              li_data['poster_path'] = item['poster_path']
              data['results'].append(li_data)
       return data

