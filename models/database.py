from app import db
from werkzeug.security import generate_password_hash, check_password_hash

# ユーザー情報
class Users(db.Model):
    __tablename__ = 'Users'
    # ID番号
    id = db.Column(db.Integer, primary_key=True)
    # ユーザー名
    name = db.Column(db.String(29))
    # パスワード
    password_hash = db.Column(db.String(255))
    # パスワードをセット
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    # パスワードを確認
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# お気に入り情報
class Records(db.Model):
    __tablename__ = 'Records'
    # ID番号
    id = db.Column(db.Integer, primary_key=True)
    # 作品・人物ID
    movie_id = db.Column(db.Integer)