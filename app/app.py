from typing import List, Dict, Any, Tuple
import simplejson as json
from flask import Flask, request, Response, redirect
from flask import render_template
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor

app = Flask(__name__)
mysql = MySQL(cursorclass=DictCursor)
app = Flask(__name__,template_folder='template')


app.config['MYSQL_DATABASE_HOST'] = 'db'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_DB'] = 'faithfulData'
mysql.init_app(app)


@app.route('/', methods=['GET'])
def index():
    user = {'username': 'Old Faithful Eruptions'}
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblfaithfulImport')
    result = cursor.fetchall()
    return render_template('index.html', title='Home', user=user, eruptions=result)


@app.route('/view/<int:eruption_id>', methods=['GET'])
def record_view(eruption_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblfaithfulImport WHERE eruption_id=%s', eruption_id)
    result = cursor.fetchall()
    return render_template('view.html', title='View Form', eruption=result[0])


@app.route('/edit/<int:eruption_id>', methods=['GET'])
def form_edit_get(eruption_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblfaithfulImport WHERE eruption_id=%s', eruption_id)
    result = cursor.fetchall()
    return render_template('edit.html', title='Edit Form', eruption=result[0])


@app.route('/edit/<int:eruption_id>', methods=['POST'])
def form_update_post(eruption_id):
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('Eruption_length_mins'), request.form.get('Eruption_wait_mins'), eruption_id)
    sql_update_query = """UPDATE tblfaithfulImport t SET t.Eruption_length_mins = %s, t.Eruption_wait_mins = %s WHERE t.eruption_id = %s """
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)

@app.route('/eruptions/new', methods=['GET'])
def form_insert_get():
    return render_template('new.html', title='New Eruption Form')


@app.route('/eruptions/new', methods=['POST'])
def form_insert_post():
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('eruption_id'), request.form.get('Eruption_length_mins'), request.form.get('Eruption_wait_mins'))
    sql_insert_query = """INSERT INTO tblfaithfulImport (eruption_id,Eruption_length_mins,Eruption_wait_mins) VALUES (%s,%s,%s) """
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/api/v1/eruptions/<int:eruption_id>', methods=['PUT'])
def api_edit(eruption_id) -> str:
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('eruption_id'), request.form.get('Eruption_length_mins'),  request.form.get('Eruption_wait_mins'), eruption_id)
    sql_update_query = """UPDATE tblfaithfulImport t SET t.eruption_id = %s, t.Eruption_length_mins = %s, t.Eruption_wait_mins = %s WHERE t.eruption_id = %s """
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()
    resp = Response(status=200, mimetype='application/json')
    return resp

@app.route('/api/v1/eruptions/<int:eruption_id>', methods=['DELETE'])
def api_delete(eruption_id) -> str:
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM tblfaithfulImport WHERE eruption_id = %s """
    cursor.execute(sql_delete_query, eruption_id)
    mysql.get_db().commit()
    resp = Response(status=210, mimetype='application/json')
    return resp


@app.route('/delete/<int:eruption_id>', methods=['POST'])
def form_delete_post(city_id):
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM tblfaithfulImport WHERE eruption_id = %s """
    cursor.execute(sql_delete_query, eruption_id)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/api/v1/eruptions', methods=['GET'])
def api_browse() -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblfaithfulImport')
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/eruptions/<int:eruption_id>', methods=['GET'])
def api_retrieve(eruption_id) -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblfaithfulImport WHERE eruption_id=%s', eruption_id)
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)