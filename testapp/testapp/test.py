from flask import Blueprint

# Blueprintのオブジェクトを生成する
test_module = Blueprint('test', __name__)

@test_module.route('/test2')
def func_2():
    return 'Test'