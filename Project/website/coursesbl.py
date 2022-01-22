from flask import Blueprint, render_template, request, url_for, redirect
from flask_mysqldb import MySQL

mysql = MySQL()

#blueprint
courses = Blueprint('courses', __name__, url_prefix='/courses')


#Courses main page
@courses.route('/')
def course():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM courses")
    data = cursor.fetchall()
    cursor.execute("SELECT college_code FROM college")
    data1 = cursor.fetchall()
    print(data)
    return render_template('course.html', courses=data, college=data1)

#Add course 
@courses.route("/addcourse", methods = ['POST'])
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
        return redirect(url_for('courses.course'))

#Edit
@courses.route("/editcourse", methods = ['POST'])
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
        return redirect(url_for('courses.course'))

#Delete
@courses.route("/delcourses/<string:course_code>", methods =['GET'])
def delcourses(course_code):
        cursor = mysql.connection.cursor()
        cursor.execute('''DELETE FROM courses WHERE course_code = %s''',(course_code,))
        mysql.connection.commit()
        cursor.close()

        return redirect(url_for('courses.course'))  