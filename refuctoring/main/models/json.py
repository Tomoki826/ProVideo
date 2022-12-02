import json, os

class JSON:
    def __init__(self):
        self.data = json.load(open('./main/static/JSON/feature.json', 'r', encoding='utf8'))
    
    # jsonデータを入手する
    def json_get(self):
        return self.data