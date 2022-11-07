from flask import request
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
        res = request.get(url, headers=self.headers_, params=params)
        return json.loads(res.text)
