from typing import List, Dict
import simplejson as json
from flask import Flask, request, Response, redirect
from flask import render_template
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor

app = Flask(__name__)
mysql = MySQL(cursorclass=DictCursor)

app.config['MYSQL_DATABASE_HOST'] = 'db'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_DB'] = 'gradesData'
mysql.init_app(app)


@app.route('/', methods=['GET'])
def index():
    user = {'username': 'Sakthi'}
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM grades')
    result = cursor.fetchall()
    return render_template('index.html', title='Home', user=user, grades=result)


@app.route('/view/<int:grade_SSN>', methods=['GET'])
def record_view(grade_SSN):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM grades WHERE SSN=%s', grade_SSN)
    result = cursor.fetchall()
    return render_template('view.html', title='View Form', grade=result[0])


@app.route('/edit/<int:grade_SSN>', methods=['GET'])
def form_edit_get(grade_SSN):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM grades WHERE SSN=%s', grade_SSN)
    result = cursor.fetchall()
    return render_template('edit.html', title='Edit Form', grade=result[0])


@app.route('/edit/<int:grade_SSN>', methods=['POST'])
def form_update_post(grade_SSN):
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('First_name'), request.form.get('Last_name'), request.form.get('Test1'),
                 request.form.get('Test2'), request.form.get('Test3'), request.form.get('Test4'), request.form.get('Final'), request.form.get('Grade'))
    sql_update_query = """UPDATE grades t SET t.First_name = %s, t.Last_name = %s, t.Test1 = %s, t.Test2 = %s, t.Test3 = %s, t.Test4 = %s, t.Final = 
    %s, t.Grade = %s WHERE t.SSN = %s """
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/grades/new', methods=['GET'])
def form_insert_get():
    return render_template('new.html', title='Students Grades')


@app.route('/grades/new', methods=['POST'])
def form_insert_post():
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('SSN'), request.form.get('First_name'), request.form.get('Last_name'),
                 request.form.get('Test1'), request.form.get('Test2'), request.form.get('Test3'), request.form.get('Test4'), request.form.get('Final'), request.form.get('Grade'))
    sql_insert_query = """INSERT INTO grades (SSN, First_name,Last_name, Test1, Test2, Test3, Test4, Final, Grade) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s) """
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/delete/<int:grade_SSN>', methods=['POST'])
def form_delete_post(grade_SSN):
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM grades WHERE SSN = %s """
    cursor.execute(sql_delete_query, grade_SSN)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/api/v1/grades', methods=['GET'])
def api_browse() -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM grades')
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/grades/<int:grade_SSN>', methods=['GET'])
def api_retrieve(grade_SSN) -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM grades WHERE SSN=%s', grade_SSN)
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/grades/', methods=['POST'])
def api_add() -> str:
    resp = Response(status=201, mimetype='application/json')
    return resp


@app.route('/api/v1/grades/<int:grade_SSN>', methods=['PUT'])
def api_edit(grade_SSN) -> str:
    resp = Response(status=201, mimetype='application/json')
    return resp


@app.route('/api/grades/<int:grade_SSN>', methods=['DELETE'])
def api_delete(grade_SSN) -> str:
    resp = Response(status=210, mimetype='application/json')
    return resp


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)