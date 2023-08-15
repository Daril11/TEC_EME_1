from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

import MySQLdb.cursors
import json

app = Flask(__name__)

# MySQL Connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'example_user'
app.config['MYSQL_PASSWORD'] = 'mysql'
app.config['MYSQL_DB'] = 'example'
app.config['MYSQL_PORT'] = 3306

# settings
app.secret_key = 'mysecretkey'

mysql = MySQL(app)

# method for listing students
@app.route('/', methods = ['GET'])
def index():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    sql = 'SELECT id, first_name, last_name, city, semester FROM student'
    cursor.execute(sql)
    data = cursor.fetchall()
    return render_template('index.html', students = data)

# method to add new student
@app.route('/add', methods = ['POST'])
def add_student():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        city = request.form['city']
        semester = request.form['semester']
        cursor = mysql.connection.cursor()
        sql = 'INSERT INTO student(first_name, last_name, city, semester) VALUES (%s, %s, %s, %s)'
        data = (first_name, last_name, city, semester)
        cursor.execute(sql, data)
        mysql.connection.commit()
        flash('Student added successfully')
        return redirect(url_for('index'))

# method to obtain a student
@app.route('/edit', methods = ['POST'])
def get_student():
    if request.method == 'POST':
        id = request.form['id']
        cursor = mysql.connection.cursor()
        sql = 'SELECT id, first_name, last_name, city, semester FROM student WHERE id = %s'
        cursor.execute(sql, (id,))
        data = cursor.fetchall()
        return render_template('edit.html', student = data[0])

# method for updating a student
@app.route('/update', methods = ['POST'])
def update_student():
    if request.method == 'POST':
        id = request.form['id']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        city = request.form['city']
        semester = request.form['semester']
        cursor = mysql.connection.cursor()
        sql = 'UPDATE student SET first_name = %s, last_name = %s, city = %s, semester = %s WHERE id = %s'
        data = (first_name, last_name, city, semester, id)
        cursor.execute(sql, data)
        mysql.connection.commit()
        flash('Student updated successfully')
        return redirect(url_for('index'))

# method for removing a student
@app.route('/delete', methods = ['POST'])
def delete_student():
    if request.method == 'POST':
        id = request.form['id']
        cursor = mysql.connection.cursor()
        cursor.execute('DELETE FROM student WHERE id = %s', (id,))
        mysql.connection.commit()
        flash('Student removed successfully')
        return redirect(url_for('index'))

# method to get a json
@app.route('/list_json', methods=['GET'])
def student_list_json():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    sql = 'SELECT id, first_name, last_name, city, semester FROM student'
    cursor.execute(sql)
    data = cursor.fetchall()
    return json.dumps(data)

# run the application
if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 81, debug = True)