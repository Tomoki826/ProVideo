from main import api_key
from main.models.TMDB import TMDB
from main.models.enum import Search
from main.models.genre import Genre
from main.models.kanji import FIRST_KANJI, SECOND_KANJI
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
              # 日本語データのインポート
              self.jp = re.compile(f'[ 0-9ぁ-ヶァ-ヶｦ-ﾟ{FIRST_KANJI}{SECOND_KANJI}]+$')

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
              # 作品タイトル
              if 'adult' not in item:
                     data['adult'] = 'false'
              if 'title' in item:
                     data['title'] = item['title']
              elif 'name' in item:
                     data['title'] = item['name']
              elif 'original_title' in item:
                     data['title'] = item['original_title']
              elif 'original_name' in item:
                     data['title'] = item['original_name']
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
              # ポスター画像
              if 'poster_path' in item:
                     data['poster_path'] = item['poster_path']
              else:
                     data['poster_path'] = ''
              # メディアタイプ
              data['videos'] = True
              match self.data['search_type']:
                     case Search.MOVIES:
                            data['media_type'] = '映画'
                     case Search.DISCOVER_MOVIE:
                            data['media_type'] = '映画'
                     case Search.TVSHOWS:
                            data['media_type'] = 'テレビ・配信番組'
                     case Search.DISCOVER_TV:
                            data['media_type'] = 'テレビ・配信番組'
                     case Search.MULTI:
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
              # 日本語名を検索 (非同期処理で高速化？)
              """
              soup = TMDB(api_key).person_id(int(item['id']))
              if 'also_known_as' in soup:
                     for item2 in soup['also_known_as']:
                            if self.jp.fullmatch(item2) != None:
                                   data['title'] = item2
                                   break
                     else:
                            data['title'] = item['name']
              """
              data['title'] = item['name']
              # 職業
              print(item.get('known_for_department'))
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
              # ポスター画像
              if 'profile_path' in item:
                     data['poster_path'] = item['profile_path']
              else:
                     data['poster_path'] = ''
              # 出演作
              data['known_for'] = []
              if 'known_for' in item:
                     for item2 in item['known_for']:
                            li = {}
                            # ポスター画像
                            if 'poster_path' in item2:
                                   li['poster_path'] = item2['poster_path']
                            else:
                                   continue
                            # id
                            li['id'] = item2['id']
                            # タイトル
                            if 'title' in item2:
                                   li['title'] = item2['title']
                            elif 'name' in item2:
                                   li['title'] = item2['name']
                            elif 'original_title' in item2:
                                   li['title'] = item2['original_title']
                            elif 'original_name' in item2:
                                   li['title'] = item2['original_name']
                            else:
                                   li['title'] = '(タイトル情報なし)'
                            data['known_for'].append(li)
              # メディアタイプ
              data['videos'] = False
              if item.get('adult') == True:
                     data['media_type'] = 'アダルト'
              else:
                     data['media_type'] = '人物'
              return data
