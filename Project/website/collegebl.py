from flask import Blueprint, render_template, request, flash, url_for, redirect
from flask_mysqldb import MySQL

mysql = MySQL()

colleges = Blueprint('colleges', __name__, url_prefix='/colleges')



#main page
@colleges.route('/')
def college():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM college")
    data = cursor.fetchall()
    print(data)
    return render_template('college.html', college=data)

        

#edit functions
@colleges.route("/editcollege", methods = ['POST'])
def editcollege():
    #requests input from webpage
    if request.method == 'POST':
        college_code = request.form['college_code']
        college_name = request.form['college_name']
    
        #plug inputs into database
        cursor = mysql.connection.cursor()
        cursor.execute(''' UPDATE college SET college_name=%s WHERE college_code=%s ''', (college_code,college_name,))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('colleges.college'))

