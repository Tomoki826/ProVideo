from main import api_key
from main.models.TMDB import TMDB
from main.models.enum import Search
from main.models.genre import Genre
from main.models.config import SENSITIVE_SEARCH
import re, datetime

# 検索情報をフォーマットする
class Search_Data:

       # 初期設定
       def __init__(self, search_type, page, raw_data, keywords=''):
              self.data = {}
              self.raw_data = raw_data
              self.data['keywords'] = keywords
              self.data['current_page'] = page
              self.data['max_page'] = (raw_data['total_results'] - 1) // 20 + 1
              self.data['total_results'] = raw_data['total_results']
              # 検索タイプ
              self.data['search_type'] = search_type
              if search_type == Search.MOVIES or search_type == Search.TVSHOWS or search_type == Search.MULTI or search_type == Search.PERSON:
                     self.data['search_type-btn'] = int(search_type)
              else:
                     self.data['search_type-btn'] = int(Search.MULTI)
              # 検索データの整理
              self.data['results'] = []

       # 検索情報をフォーマット
       def arrange(self):
              for item in self.raw_data['results']:
                     if self.data['search_type'] == Search.PERSON or item.get('media_type') == 'person':
                            data = self.__person_results_type(item)
                     else:
                            data = self.__video_type(item)
                     self.data['results'].append(data)
              return self.data

       # 作品データを修正
       def __video_type(self, item):
              data = {}
              # id
              data['id'] = item['id']
              # 作品タイトル
              if 'adult' not in item:
                     data['adult'] = 'false'
              if 'title' in item:
                     data['title'] = item['title'].strip()
              elif 'name' in item:
                     data['title'] = item['name'].strip()
              elif 'original_title' in item:
                     data['title'] = item['original_title'].strip()
              elif 'original_name' in item:
                     data['title'] = item['original_name'].strip()
              else:
                     data['title'] = '(タイトル情報なし)'
              # 公開日
              if 'release_date' in item:
                     # 日付文字列の正規表現パターンと一致するか確認
                     if re.fullmatch(r'\d{4}-\d{2}-\d{2}', item['release_date']):
                            dte = datetime.datetime.strptime(item['release_date'], '%Y-%m-%d')
                            data['openday'] = '公開日: ' + str(dte.year) + '年' + str(dte.month) + '月' + str(dte.day) + '日'
              elif 'first_air_date' in item:
                     # 日付文字列の正規表現パターンと一致するか確認
                     if re.fullmatch(r'\d{4}-\d{2}-\d{2}', item['first_air_date']):
                            dte = datetime.datetime.strptime(item['first_air_date'], '%Y-%m-%d')
                            data['openday'] = '公開日: ' + str(dte.year) + '年' + str(dte.month) + '月' + str(dte.day) + '日'
              if 'openday' not in data:
                     data['openday'] = '公開日: 不明'
              # ジャンル
              if 'genre_ids' not in item or item.get('genre_ids') == []:
                     data['genre'] = 'ジャンル: 不明'
              else:
                     data['genre'] = 'ジャンル: '
                     for id in item['genre_ids']:
                             data['genre'] += Genre().name_get(id) + ', '
                     data['genre'] = data['genre'][:-2]
              # 注目度
              data['popularity'] = item.get('popularity', 0)
              # ポスター画像
              data['poster_path'] = item.get('poster_path', '')
              # メディアタイプ
              match self.data['search_type']:
                     case Search.MOVIES:
                            data['media_type'] = '映画'
                            data['data_type'] = 'movie'
                     case Search.DISCOVER_MOVIE:
                            data['media_type'] = '映画'
                            data['data_type'] = 'movie'
                     case Search.TVSHOWS:
                            data['media_type'] = 'テレビ・配信番組'
                            data['data_type'] = 'tv'
                     case Search.DISCOVER_TV:
                            data['media_type'] = 'テレビ・配信番組'
                            data['data_type'] = 'tv'
                     case Search.MULTI:
                            data['data_type'] = item.get('media_type')
                            if 'media_type' not in item:
                                   data['media_type'] = '不明'
                            elif item.get('adult') == True:
                                   data['media_type'] = 'アダルト'
                            else:
                                   match item['media_type']:
                                          case 'movie':
                                                 data['media_type'] = '映画'
                                          case 'tv':
                                                 data['media_type'] = 'テレビ・配信番組'
                                          case _:
                                                 data['media_type'] = '不明' 
              return data           


       # 人物データを修正
       def __person_results_type(self, item):
              data = {}
              # 名前
              data['title'] = item['name'].strip()
              data['id'] = item['id']
              # 職業
              match item.get('known_for_department'):
                     case "Acting":
                            data['known_videos'] = "主な出演作品"
                            match item.get('gender'):
                                   case 1:
                                          data['department'] = "職業: タレント・女優"
                                   case 2:
                                          data['department'] = "職業: タレント・俳優"
                                   case _:
                                          data['department'] = "職業: タレント"
                     case "Production":
                            data['known_videos'] = "主な作品"
                            data['department'] = "職業: プロデューサー"
                     case "Visual Effects":
                            data['known_videos'] = "主な作品"
                            data['department'] = "職業: エフェクト・CGクリエイター"
                     case "Directing":
                            data['known_videos'] = "主な監督作品"
                            data['department'] = "職業: ディレクター・監督"
                     case "Sound":
                            data['known_videos'] = "主な作品"
                            data['department'] = "職業: ミュージシャン"
                     case "Writing":
                            data['known_videos'] = "主な脚本作品"
                            data['department'] = "職業: 脚本家"
                     case "Editing":
                            data['known_videos'] = "主な作品"
                            data['department'] = "職業: 映像クリエイター"
                     case "Art":
                            data['known_videos'] = "主な作品"
                            data['department'] = "職業: デザイナー"
                     case _:
                            data['known_videos'] = "主な作品"
                            data['department'] = "職業: 不明"

              # 性別
              if item.get('gender') == 1:
                     data['gender'] = "性別: 女性"
              elif item.get('gender') == 2:
                     data['gender'] = "性別: 男性"
              else:
                     data['gender'] = "性別: その他・不明"
              # 注目度
              data['popularity'] = item.get('popularity', 0)
              # ポスター画像
              data['poster_path'] = item.get('profile_path', '')
              # 出演作
              data['known_for'] = []
              if 'known_for' in item:
                     for item2 in item['known_for']:
                            li = {}
                            # ポスター画像
                            if 'poster_path' in item2 and (item2.get('adult') != True or (item2.get('adult') == True and SENSITIVE_SEARCH == True)):
                                   li['poster_path'] = item2['poster_path']
                            else:
                                   continue
                            # id
                            li['id'] = item2['id']
                            # タイトル
                            if 'title' in item2:
                                   li['title'] = item2['title'].strip()
                            elif 'name' in item2:
                                   li['title'] = item2['name'].strip()
                            elif 'original_title' in item2:
                                   li['title'] = item2['original_title'].strip()
                            elif 'original_name' in item2:
                                   li['title'] = item2['original_name'].strip()
                            else:
                                   li['title'] = '(タイトル情報なし)'
                            data['known_for'].append(li)
              # メディアタイプ
              data['data_type'] = 'person'
              if item.get('adult') == True:
                     data['media_type'] = 'アダルト'
              else:
                     data['media_type'] = '人物'
              return data
