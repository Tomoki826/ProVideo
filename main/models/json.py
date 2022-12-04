import json, os

class JSON:
    def __init__(self, filename):
        with open(filename, 'r', encoding='utf8') as file:
            self.data = json.load(file)
    
    # jsonデータを入手する
    def get_json(self):
        return self.data