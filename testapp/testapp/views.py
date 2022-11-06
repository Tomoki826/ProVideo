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
def add_amployee():
    if request.method == 'GET':
        return render_template('add_employee.html')
    if request.method == 'POST':
        employee = Employee(
            name='Tanaka',
            mail="aaa@aa.com",
            is_remote=False,
            department="develop",
            year=2
        )
        db.session.add(employee)
        db.session.commit()
        return redirect(url_for('janken.sample_form'))