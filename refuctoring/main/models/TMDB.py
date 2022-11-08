import requests
import json

class TMDB:
    def __init__(self, token):
        self.token = token
        self.headers_ = {'Authorization': f'Bearer {self.token}', 'Content-Type': 'application/json;charset=utf-8'}
        self.base_url_ = 'https://api.themoviedb.org/3/'
        self.img_base_url_ = 'https://image.tmdb.org/t/p/w500'
        self.language = 'ja'
        self.region = 'JP'
    
    # URLを生成する
    def _json_by_get_request(self, url, params={}):
        params['language'] = self.language
        params['region'] = self.region
        print(url, params)
        res = requests.get(url, headers=self.headers_, params=params)
        return json.loads(res.text)
    
    # キーワードに部分一致する映画タイトルを取得
    def search_movies(self, with_keywords, page):
        params = {'query': with_keywords}
        params['page'] = page
        url = f'{self.base_url_}search/movie'
        return self._json_by_get_request(url, params)

    # キーワードに部分一致するテレビ番組を取得
    def search_tvshows(self, with_keywords, page):
        params = {'query': with_keywords}
        params['page'] = page
        url = f'{self.base_url_}search/tv'
        return self._json_by_get_request(url, params)

    # キーワードに部分一致するテレビ番組・映画・タレントをまとめて取得
    def search_multi(self, with_keywords, page, adult=False):
        params = {'query': with_keywords}
        params['page'] = page
        if adult:
            params['include_adult'] = 'true'
        else:
            params['include_adult'] = 'false'
        url = f'{self.base_url_}search/multi'
        return self._json_by_get_request(url, params)