from flask import Flask, render_template, Response, request, redirect, url_for, jsonify
import cv2
import datetime
import time
import os
import sys
import numpy as np
import detection
# import db


global capture, rec_frame, switch, face, rec, out
capture = 0
switch = 1
rec = 0
now = datetime.datetime.now()
date = str(now.strftime("%d-%m-%Y"))
dir = os.listdir('./static/img/')

try:
    directory_path = './Attendance/{}'.format(date)
    os.mkdir(directory_path)
except OSError as error:
    pass

app = Flask(__name__, template_folder='./templates')
app.secret_key = 'None'
app.secret_date_and_time = ''
app.secret_frame = 0

camera = cv2.VideoCapture(0)


@app.route('/')
def home():
    if dir is not None and len(dir) != 0:
        try:
            os.remove("./static/img/temp.png")
        except FileNotFoundError:
            pass
    else:
        pass
    return render_template('login.html')


@app.route('/home.html')
def returnToHome():
    if dir is not None and len(dir) != 0:
        try:
            os.remove("./static/img/temp.png")
        except FileNotFoundError:
            pass
    else:
        pass
    return render_template('home.html')


@app.route('/index.html')
def index():
    if dir is not None and len(dir) != 0:
        try:
            os.remove("./static/img/temp.png")
        except FileNotFoundError:
            pass
    else:
        pass
    return render_template('index.html')


@app.route('/review')
def review():
    return render_template('review.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    # response = db.signin()
    return redirect(url_for('returnToHome'))


@app.route('/detect', methods=['POST', 'GET'])
def detect():
    p = os.path.sep.join(
        [directory_path, "{}_{}.png".format(app.secret_key, app.secret_date_and_time)])
    print(p)
    cv2.imwrite(p, app.secret_frame)
    time.sleep(10)
    if app.secret_key == 'None':
        message = "No face detected"
    else:
        message = "Marked attendance for {}".format(app.secret_key)
    print(message)
    return jsonify(message)


def gen_frames():
    global out, capture, rec_frame
    while True:
        success, frame = camera.read()
        if success:
            if (capture):
                capture = 0
                cv2.imwrite('./static/img/temp.png', frame)
                app.secret_frame = frame
                output = detection.predict(frame)
                app.secret_key = output
                print(app.secret_key)
                print('Prediction--', output)
                # result()

            try:
                ret, buffer = cv2.imencode('.jpg', cv2.flip(frame, 1))
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            except Exception as e:
                pass

        else:
            pass


@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/requests', methods=['POST', 'GET'])
def tasks():
    global switch, camera
    if request.method == 'POST':
        if request.form.get('click') == 'Capture':
            global capture
            capture = 1
            app.secret_date_and_time = now.strftime("%d-%m-%Y_%I.%M")

    elif request.method == 'GET':
        return redirect('/')
    return render_template('review.html', image_url='static/img/temp.png')


if __name__ == '__main__':
    app.run()

camera.release()
cv2.destroyAllWindows()
