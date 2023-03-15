from flask import Flask, redirect, render_template, request, url_for
from flask_mysqldb import MySQL
from os import environ
from datetime import datetime

app = Flask(__name__)
app.secret_key = environ.get('SECRET_KEY')
app.config['MYSQL_HOST'] = environ.get('DB_HOST')
app.config['MYSQL_PASSWORD'] = environ.get('DB_PASSWORD')
app.config['MYSQL_DB'] = environ.get('DB_DATABASE')
app.config['MYSQL_USER'] = environ.get('DB_USERNAME')
mysql = MySQL(app)

@app.route('/')
def home() : # view function
    return render_template("home.html")

@app.route('/about')
def about() :
    return render_template("about.html")



@app.route('/lists/post', methods=["GET", "POST"])
def postlist() :
    if request.method == 'GET' :
        return render_template("lists/add.html")
    if request.method == 'POST':
        title = request.form['title']
        tag = request.form['tag']
        description = request.form['description']
        due_date = request.form['due_date']
        cursor = mysql.connection.cursor()
        cursor.execute('''INSERT INTO lists(title,tag,description,due_date) VALUES(%s,%s,%s,%s)''',(title, tag, description, due_date))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('lists'))
    
    # return render_template('list.html')

@app.route('/lists')
def lists() :
    cursor = mysql.connection.cursor()
    cursor.execute('''SELECT * FROM lists''')
    lists = cursor.fetchall()
    cursor.close()

    return render_template('lists/get.html', lists=lists)

@app.route('/lists/<id>')
def showlist(id) :
    cursor = mysql.connection.cursor()
    cursor.execute('''SELECT * FROM lists WHERE list_id=%s''', (id))
    todo = cursor.fetchone()
    cursor.close()
    return render_template("lists/show.html", todo = todo)
# return redirect(url_for('lists'))

@app.route('/lists/<id>/edit', methods=["GET", "POST"])
def editlist(id) :
    if request.method == 'POST':
        title = request.form['title']
        tag = request.form['tag']
        description = request.form['description']
        due_date = request.form['due_date']

        cursor = mysql.connection.cursor()
        cursor.execute('''UPDATE lists SET title=%s,tag=%s,description=%s,due_date=%s WHERE list_id=%s''',(title, tag, description, due_date, id))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('lists'))
    else :
        cursor = mysql.connection.cursor()
        cursor.execute('''SELECT * FROM LISTS WHERE list_id=%s''', (id, ))
        lists = cursor.fetchone()
        cursor.close()
        return render_template("lists/edit.html", lists=lists)
    
@app.route('/lists/<id>/delete', methods=["GET"])
def deletelist(id) :
    cursor = mysql.connection.cursor()
    cursor.execute('''DELETE FROM LISTS WHERE list_id=%s''', (id, ))
    mysql.connection.commit()
    cursor.close()
    return redirect(url_for('lists'))

if __name__ == "__main__" :
    app.run()