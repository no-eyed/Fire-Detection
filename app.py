from flask import Flask, request, render_template, flash, redirect
import os
from werkzeug.utils import secure_filename
import cv2

import check as ai
# import numpy as np
# import pandas as pd
# from sklearn.preprocessing import StandardScaler
UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff', 'svg'}

app=Flask(__name__)
app.secret_key = 'super secret key'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def preProcessImage(filename):
    print(f"Function is appning for '{filename}'")
    img = cv2.imread(f"uploads/{filename}")
    height, width, channels = img.shape
    aspectratio = width / height
    new_width = aspectratio * 300
    new_height = 300
    new_img = cv2.resize(img, (int(new_width), int(new_height)), interpolation = cv2.INTER_LINEAR) 
    cv2.imwrite(f"static/inputs/image.jpg", new_img)
    return filename


@app.route('/', methods = ['GET'])
def home():
    return render_template('home.html')

@app.route('/upload', methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        if 'file' not in request.files:
            flash('No file part')
            return "Error occured"
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return "No Image Selected"
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            new = preProcessImage(filename)
            ai.check()
            print(new)
            flash(f"Your Image has been processed ")
            # print(<a href='/static/results/boxed_image.jpg' target='_blank'>Here</a>)
            return render_template('result.html')
        
    return render_template('home.html')

# @app.route('/redirect-home', methods=["GET"])
# def redirect-home():
#     return redirect('/home', code=302)

if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0",port=8000)



