from testapp import app
from flask_sqlalchemy import SQLAlchemy

# モジュールを導入
from testapp.test import test_module
app.register_blueprint(test_module)
from testapp.janken import janken_module
app.register_blueprint(janken_module)

# アプリを実行
if __name__ == '__main__':
    app.run()
    """
    from testapp import db
    with app.app_context():
        db.create_all()
    """