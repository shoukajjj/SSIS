from flask import Flask,render_template, request, redirect
from flask_mysqldb import MySQL
from flask.helpers import url_for
import cloudinary
from dotenv import load_dotenv
import os
import cloudinary.uploader




load_dotenv()
app = Flask(__name__)


app.config['MYSQL_HOST'] = os.getenv("DB_HOST")
app.config['MYSQL_USER'] = os.getenv("DB_USER")
app.config['MYSQL_PASSWORD'] = os.getenv("DB_PASSWORD")
app.config['MYSQL_DB'] = os.getenv("DB_DB")


cloudinary.config( 
  cloud_name = os.getenv("cloud_name"),
  api_key = os.getenv("api_key"),
  api_secret = os.getenv("api_secret")
)

mysql = MySQL(app)

from coursesbl import courses
from collegebl import colleges

app.register_blueprint(colleges)
app.register_blueprint(courses)



#Cloudinary Upload
def uploadImage(image):
    uploadResult = cloudinary.uploader.upload(image, folder="SSIS-Profile-Icons",
                                              eager=[{"width": 50, "height": 50, "crop": "fill"}])

    return uploadResult['secure_url'], uploadResult['eager'][0]['secure_url']


#Main student page
@app.route('/')
def student():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM student ORDER BY id_number")
    data = cursor.fetchall()
    cursor.execute("SELECT course_code FROM courses")
    data1 = cursor.fetchall()
    print(data)
    return render_template('base.html',student = data, courses = data1 )


#Add student       
@app.route("/add", methods = ['POST'])
def add():
        #requests input from webpage
    if request.method == 'POST':
        id_number = request.form['id_num']
        last_name = request.form['lname']
        first_name = request.form['fname']
        course_code = request.form['course_code']
        year_level = request.form['year']
        gender = request.form['gender']
        image = request.files['file']

        img_url = uploadImage(image)

        #plug inputs into database
        cursor = mysql.connection.cursor()
        cursor.execute('''INSERT INTO student VALUES (%s,%s,%s,%s,%s,%s,%s) ''', (id_number, first_name, last_name, course_code, year_level, gender,img_url, ))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('student'))


#Edit student
@app.route("/editstudent", methods = ['POST'])
def editstudent():
    #requests input from webpage
    if request.method == 'POST':
        id_number = request.form['id_num']
        last_name = request.form['lname']
        first_name = request.form['fname']
        course_code = request.form['courses_code']
        year_level = request.form['year']
        gender = request.form['gender']
        image = request.files['file']

        
        if image:
            img_url = uploadImage(image)
            cursor = mysql.connection.cursor()
            cursor.execute('''UPDATE student SET img_url=%s WHERE id_number=%s ''',
            (id_number,img_url,))
            mysql.connection.commit()

        #plug inputs into database
        cursor = mysql.connection.cursor()
        cursor.execute('''UPDATE student SET last_name=%s,first_name=%s,course_code=%s,year_level=%s,gender=%s,img_url=%s WHERE id_number=%s ''',
        (id_number,last_name, first_name, course_code, year_level, gender,img_url,))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('student')) 


#Delete function
@app.route("/delstudent/<string:id_number>", methods =['GET'])
def delstudent(id_number):
        cursor = mysql.connection.cursor()
        cursor.execute('''DELETE FROM student WHERE id_number = %s''',(id_number,))
        mysql.connection.commit()
        cursor.close()

        return redirect(url_for("student"))   




if __name__ == '__main__':
    app.run(debug=True)
