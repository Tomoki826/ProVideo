from models.json import JSON

class Icon:

    def __init__(self):
        self.json = JSON('./static/JSON/famous_providers.json').get_json()

    # アイコン画像のpathが適切か
    def path_check(self, path):
        for item in self.json['results']:
            if item.get('alternative_path') == path:
                return item['logo_path']
        return path