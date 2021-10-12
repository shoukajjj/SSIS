from flask import Flask,render_template, request, redirect
from flask_mysqldb import MySQL
from flask.helpers import url_for





app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'ajmolijon0911'
app.config['MYSQL_DB'] = 'stud_db'



mysql = MySQL(app)





#main pages
@app.route('/')
def student():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM student ORDER BY id_number")
    data = cursor.fetchall()
    cursor.execute("SELECT course_code FROM courses")
    data1 = cursor.fetchall()
    print(data)
    return render_template('base.html',student = data, courses = data1 )


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
    cursor.execute("SELECT college_code FROM college")
    data1 = cursor.fetchall()
    print(data)
    return render_template('course.html', courses=data, college=data1)


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
        course_code = request.form['course_code']
        year_level = request.form['year']
        gender = request.form['gender']

        #plug inputs into database
        cursor = mysql.connection.cursor()
        cursor.execute('''INSERT INTO student VALUES(%s,%s,%s,%s,%s,%s)''',(id_number, first_name, last_name, course_code, year_level, gender))
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
        cursor.execute('''INSERT INTO courses VALUES(%s,%s,%s)''',(course_code,course_name,college_code))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('courses'))




#edit functions
@app.route("/editcollege", methods = ['POST'])
def editcollege():
    #requests input from webpage
    if request.method == 'POST':
        college_code = request.form['college_code']
        college_name = request.form['college_name']
    
        #plug inputs into database
        cursor = mysql.connection.cursor()
        cursor.execute('''UPDATE college SET  college_name=%s WHERE college_code=%s''',(college_code,college_name))
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
        course_code = request.form['course_code']
        year_level = request.form['year']
        gender = request.form['gender']

        #plug inputs into database
        cursor = mysql.connection.cursor()
        cursor.execute('''UPDATE student SET first_name=%s,last_name=%s,course_code=%s,year_level=%s,gender=%s WHERE id_number=%s ''',
        ( first_name, last_name, course_code, year_level, gender,id_number))
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
        cursor.execute('''UPDATE courses SET course_name=%s,college_code=%s WHERE course_code=%s''',(course_name,college_code, course_code))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('courses'))
       
       




#delete functions

@app.route("/delcourses/<string:course_code>", methods =['GET'])
def delcourses(course_code):
        cursor = mysql.connection.cursor()
        cursor.execute('''DELETE FROM courses WHERE course_code = %s''',(course_code,))
        mysql.connection.commit()
        cursor.close()

        return redirect(url_for("courses"))   


@app.route("/delstudent/<string:id_number>", methods =['GET'])
def delstudent(id_number):
        cursor = mysql.connection.cursor()
        cursor.execute('''DELETE FROM student WHERE id_number = %s''',(id_number,))
        mysql.connection.commit()
        cursor.close()

        return redirect(url_for("student"))   




  



if __name__ == '__main__':
    app.run(debug=True)
