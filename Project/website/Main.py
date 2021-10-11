from flask import Flask,render_template, request, redirect
from flask_mysqldb import MySQL
from flask.helpers import url_for





app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'ajmolijon0911'
app.config['MYSQL_DB'] = 'stud_db'



mysql = MySQL(app)

@app.route('/')
def base():
   return render_template('base.html')



#main pages
@app.route('/student')
def student():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM student ORDER BY id_number")
    data = cursor.fetchall()
    print(data)
    return render_template('student.html',student = data)


@app.route('/college')
def college():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM college")
    data = cursor.fetchall()
    print(data)
    return render_template('college.html', college=data)


@app.route('/courses')
def courses():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM courses")
    data = cursor.fetchall()
    print(data)
    return render_template('course.html', courses=data)



#add functions

@app.route("/addcollege", methods = ['POST'])
def addcollege():
    #requests input from webpage
    if request.method == 'POST':
        college_code = request.form['college_code']
        college_name = request.form['college_name']
    
        #plug inputs into database
        cursor = mysql.connection.cursor()
        cursor.execute('''INSERT INTO college VALUES(%s,%s)''',(college_code,college_name))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('college'))
        

@app.route("/add", methods = ['GET','POST'])
def add():
    #requests input from webpage
    if request.method == 'POST':
        id_number = request.form['id_num']
        last_name = request.form['lname']
        first_name = request.form['fname']
        course = request.form['course']
        year_level = request.form['year']
        gender = request.form['gender']

        #plug inputs into database
        cursor = mysql.connection.cursor()
        cursor.execute('''INSERT INTO student VALUES(%s,%s,%s,%s,%s,%s)''',(id_number, first_name, last_name, course, year_level, gender))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('student'))


@app.route("/addcourse", methods = ['POST'])
def addcourse():
    #requests input from webpage
    if request.method == 'POST':
        course_code = request.form['course_code']
        course_name = request.form['course_name']
        college_code = request.form['college_code']
    
        #plug inputs into database
        cursor = mysql.connection.cursor()
        cursor.execute('''INSERT INTO courses VALUES(%s,%s)''',(course_code,course_name))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('course'))




#edit functions
@app.route("/editcollege", methods = ['POST'])
def aeditcollege():
    #requests input from webpage
    if request.method == 'POST':
        college_code = request.form['college_code']
        college_name = request.form['college_name']
    
        #plug inputs into database
        cursor = mysql.connection.cursor()
        cursor.execute('''UPDATE college set college_code=%s, college_name=%s ''',(college_code,college_name))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('college'))

@app.route("/editstudent", methods = ['GET','POST'])
def editstudent():
    #requests input from webpage
    if request.method == 'POST':
        id_number = request.form['id_num']
        last_name = request.form['lname']
        first_name = request.form['fname']
        course = request.form['course']
        year_level = request.form['year']
        gender = request.form['gender']

        #plug inputs into database
        cursor = mysql.connection.cursor()
        cursor.execute('''UPDATE student set id_number=%s,first_name=%s,last_name=%s,course=%s,year_level=%s,gender=%s ''',
        (id_number, first_name, last_name, course, year_level, gender))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('student')) 


@app.route("/editcourse", methods = ['POST'])
def editcourse():
    #requests input from webpage
    if request.method == 'POST':
        course_code = request.form['course_code']
        course_name = request.form['course_name']
        college_code = request.form['college_code']
    
        #plug inputs into database
        cursor = mysql.connection.cursor()
        cursor.execute('''UPDATE courses set course_code=%s,course_name=%s,college_code=%s)''',(course_code,course_name,college_code))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('course'))
       
       




#delete functions

@app.route("/delcollege/<string:college_code>", methods =['GET'])
def delcollege(college_code):
        cursor = mysql.connection.cursor()
        cursor.execute('''DELETE FROM college WHERE college_code = %s''',(college_code,))
        mysql.connection.commit()
        cursor.close()

        return redirect(url_for("college"))   


@app.route("/delcourses/<string:course_code>", methods =['GET'])
def delcourses(course_code):
        cursor = mysql.connection.cursor()
        cursor.execute('''DELETE FROM college WHERE college_code = %s''',(course_code,))
        mysql.connection.commit()
        cursor.close()

        return redirect(url_for("course"))   


@app.route("/delstudent/<string:id_num>", methods =['GET'])
def delstudent(id_number):
        cursor = mysql.connection.cursor()
        cursor.execute('''DELETE FROM college WHERE college_code = %s''',(id_number,))
        mysql.connection.commit()
        cursor.close()

        return redirect(url_for("student"))   




  



if __name__ == '__main__':
    app.run(debug=True)
