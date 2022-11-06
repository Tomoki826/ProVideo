from flask import render_template, request
from testapp import app

#app.register_blueprint(janken_module)

@app.route("/")
def index():
    my_dict = {
        'insert_something1': 'views.pyのinsert_something1部分です。',
        'insert_something2': 'views.pyのinsert_something2部分です。',
        'test_titles': ['title1', 'title2', 'title3']
    }
    return render_template('index.html', my_dict=my_dict)

@app.route('/test')
def other1():
    return render_template('index2.html')

@app.route('/sampleform', methods=['GET', 'POST'])
def sample_form():
    if request.method == 'GET':
        return render_template('sampleform.html')
    if request.method == 'POST':
        print('POSTデータ受け取ったので処理します')
        req1 = request.form['data1']
        return f'POST受け取ったよ: {req1}'
    return 'error' 

