from flask import redirect,session
from flask import Flask, render_template, request, Response, jsonify
import os
from ObjectDetector import Detector
from flask_cors import CORS, cross_origin
from rehan.utils import decodeImage
import sqlite3


RENDER_FACTOR = 35

os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"
app = Flask(__name__)
CORS(app)
detector = Detector(filename="file.jpg")
app.secret_key=os.urandom(24)
conn=sqlite3.connect("E:\\programming\\projectsssss\\logindata.db",check_same_thread=False)
cursor=conn.cursor()

class objectrehan:
    def __init__(self):
        self.filename = "file.jpg"

        self.objectDetection = Detector(self.filename)



def run_inference(img_path='file.jpg'):

    result_img = detector.inference(img_path)

    try:
        os.remove(img_path)
    except:
        pass

    return result_img

@app.route("/min")
def min():

    return render_template("index.html")

@app.route("/predict", methods=['POST', 'GET'])
@cross_origin()
def predictRoute():
    try:
        image = request.json['image']
        decodeImage(image, clapp.filename)
        result = clapp.objectDetection.inference('file.jpg')

    except ValueError as val:
        print(val)
        return Response("Value not found inside  json data")
    except KeyError:
        return Response("Key value error incorrect key passed")
    except Exception as e:
        print(e)
        result = "Invalid input"
    return jsonify(result)

@app.route('/')
def home():
    return render_template('first.html')

@app.route('/about')
def about():
    return "about"

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/home')
def home1():
    if 'user_id' in session:

        return render_template('home.html')

    else:
        return redirect('/')

@app.route('/login_valid',methods=['POST'])
def login_valid():
    email=request.form.get('email')
    password=request.form.get('password')

    cursor.execute("""SELECT * FROM `logintable` WHERE `email` LIKE '{}' AND `password` LIKE '{}'"""
                   .format(email,password))
    users=cursor.fetchall()
    if len(users)>0:
        session['user_id']=users[0][0]
        return redirect('/min')
    else:
        return redirect('/')


@app.route('/add_user',methods=['POST'])
def add_user():
    name=request.form.get('uname')
    email=request.form.get('uemail')
    password=request.form.get('upassword')
    id=request.form.get('uid')

    cursor.execute("""INSERT INTO `logintable` ('id',`name`,`email`,`password`) VALUES
    ('{}','{}','{}','{}') """.format(id,name,email,password))
    conn.commit()
    cursor.execute("""SELECT * FROM `logintable` WHERE `email` LIKE '{}'""".format(email))
    myuser=cursor.fetchall()
    session['userid']=myuser[0][0]
    return redirect('/home')


@app.route('/logout')
def logout():
    session.pop('user_id')
    return redirect('/')

if __name__=="__main__":
    clapp=objectrehan()
    port=9000
    app.run(host='0.0.0.0',port=port)
