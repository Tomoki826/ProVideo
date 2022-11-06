from flask import render_template
from testapp import app

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

from flask import request, redirect, url_for
from testapp import db
from testapp.models.employee import Employee

@app.route('/add_employee', methods=['GET', 'POST'])
def add_employee():
    if request.method == 'GET':
        return render_template('add_employee.html')
    if request.method == 'POST':
        form_name = request.form.get('name')  # str
        form_mail = request.form.get('mail')  # str
        # チェックなしならFalse。str -> bool型に変換
        form_is_remote = request.form.get('is_remote', default=False, type=bool)
        form_department = request.form.get('department')  # str
        # int, データないとき０
        form_year = request.form.get('year', default=0, type=int)

        employee = Employee(
            name=form_name,
            mail=form_mail,
            is_remote=form_is_remote,
            department=form_department,
            year=form_year
        )
        db.session.add(employee)
        db.session.commit()
        return redirect(url_for('index'))

@app.route('/employees')
def employee_list():
    # 全クエリ取得
    employees = Employee.query.all()
    return render_template('employee_list.html', employees=employees)

@app.route('/employees/<int:id>')
def employee_detail(id):
    employee = Employee.query.get(id) # primary keyで単一のデータを取得
    """
    employee = Employee.query.get_or_404(id) getできない場合は404エラーを出す
    employee = Employee.query.filter(Employee.id == id).one() idが一つでない場合はエラー → try, catchで処理を工夫しよう
    """
    return render_template('employee_detail.html', employee=employee)

@app.route('/employees/<int:id>/edit', methods=['GET'])
def employee_edit(id):
    # 編集ページ表示用
    employee = Employee.query.get(id)
    return render_template('employee_edit.html', employee=employee)

@app.route('/employees/<int:id>/update', methods=['POST'])
def employee_update(id):
    employee = Employee.query.get(id)  # 更新するデータをDBから取得
    employee.name = request.form.get('name')
    employee.mail = request.form.get('mail')
    employee.is_remote = request.form.get('is_remote', default=False, type=bool)
    employee.department = request.form.get('department')
    employee.year = request.form.get('year', default=0, type=int)

    db.session.merge(employee)
    db.session.commit()
    return redirect(url_for('employee_list'))

@app.route('/employees/<int:id>/delete', methods=['POST'])  
def employee_delete(id):  
    employee = Employee.query.get(id)   
    db.session.delete(employee)  
    db.session.commit()  
    return redirect(url_for('employee_list'))