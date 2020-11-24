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
    return render_template('index.html', title='Home', user=user, cities=result)


@app.route('/view/<int:city_id>', methods=['GET'])
def record_view(city_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM grades WHERE id=%s', city_id)
    result = cursor.fetchall()
    return render_template('view.html', title='View Form', city=result[0])


@app.route('/edit/<int:city_id>', methods=['GET'])
def form_edit_get(city_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM grades WHERE id=%s', city_id)
    result = cursor.fetchall()
    return render_template('edit.html', title='Edit Form', city=result[0])


@app.route('/edit/<int:city_id>', methods=['POST'])
def form_update_post(city_id):
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('First_name'), request.form.get('Last_name'), request.form.get('Test1'),
                 request.form.get('Test2'), request.form.get('Test3'), request.form.get('Test4'), request.form.get('Final'), request.form.get('Grade') city_id)
    sql_update_query = """UPDATE grades t SET t.First_name = %s, t.Last_name = %s, t.Test1 = %s, t.Test2 = %s, t.Test3 = %s, t.Test4 = %s, t.Final = 
    %s, t.Grade = %s WHERE t.id = %s """
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/cities/new', methods=['GET'])
def form_insert_get():
    return render_template('new.html', title='New Oscar AwardForm')


@app.route('/cities/new', methods=['POST'])
def form_insert_post():
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('SSN'), request.form.get('First_name'), request.form.get('Last_name'),
                 request.form.get('Test1'), request.form.get('Test2'), request.form.get('Test3'), request.form.get('Test4'), request.form.get('Final'), request.form.get('Grade'))
    sql_insert_query = """INSERT INTO grades (SSN, First_name,Last_name, Test1, Test2, Test3, Test4, Final, Grade) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s) """
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/delete/<int:city_id>', methods=['POST'])
def form_delete_post(city_id):
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM grades WHERE id = %s """
    cursor.execute(sql_delete_query, city_id)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/api/v1/oscar', methods=['GET'])
def api_browse() -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM grades')
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/oscar/<int:city_id>', methods=['GET'])
def api_retrieve(city_id) -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM grades WHERE id=%s', city_id)
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/oscar/', methods=['POST'])
def api_add() -> str:
    resp = Response(status=201, mimetype='application/json')
    return resp


@app.route('/api/v1/oscar/<int:city_id>', methods=['PUT'])
def api_edit(city_id) -> str:
    resp = Response(status=201, mimetype='application/json')
    return resp


@app.route('/api/oscar/<int:city_id>', methods=['DELETE'])
def api_delete(city_id) -> str:
    resp = Response(status=210, mimetype='application/json')
    return resp


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)