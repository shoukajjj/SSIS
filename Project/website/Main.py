from flask import Flask,render_template, request
from flask_mysqldb import MySQL
import pymysql





app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'ajmolijon0911'
app.config['MYSQL_DB'] = 'stud_db'



mysql = MySQL(app)

@app.route('/')
def base():
   

    return render_template('base.html')


@app.route('/addstudent')
def addstudent():
    return render_template('addstudent.html')

@app.route('/student')
def student():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM student ORDER BY id_num")
    data = cursor.fetchall()
    print(data)
    return render_template('student.html',student = data)


@app.route('/college')
def college():
    return render_template('college.html')

@app.route('/course')
def course():
    return render_template('course.html')



@app.route("/add", methods = ['GET','POST'])
def add():
    #requests input from webpage
    if request.method == 'POST':
        id_num = request.form['id_num']
        fname = request.form['fname']
        lname = request.form['lname']
        course = request.form['course']
        year = request.form['year']
        gender = request.form['gender']

        #plug inputs into database
        cursor = mysql.connection.cursor()
        cursor.execute('''INSERT INTO student VALUES(%s,%s,%s,%s,%s,%s)''',(id_num, fname, lname, course, year, gender))
        mysql.connection.commit()
        cursor.close()
        return render_template('student.html')

  



if __name__ == '__main__':
    app.run(debug=True)
