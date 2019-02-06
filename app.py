# -*- coding: utf-8 -*-
"""
Created on Wed Jul 18 10:43:36 2018

@author: PATU1
"""
import flask
from flask import Flask, render_template, request
from werkzeug import secure_filename
import numpy as np
#from scipy import misc
#import imageio
import predict_rose
import os

FOLDER = 'C:/Rose_Classifier/FOLDER'
app = Flask(__name__)
app.config['FOLDER'] = FOLDER

@app.route("/")
@app.route("/index")
def index():
   return flask.render_template('index.html')    

@app.route('/predict', methods=['POST'])
def predict():
    if request.method=='POST':
        file = request.files['image']
        if not file: 
            return render_template('index.html', label="No File")
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['FOLDER'], filename)
        file.save(file_path)
        img_path = file_path
        #img = imageio.imread(file)
        #img = img[:,:,:3]
        #img = img.reshape(1, -1)
        make_prediction = predict_rose.predict_val(img_path)
        label = np.squeeze(make_prediction)
        #print(label)
        if label[0] > label[1]:
            return render_template('rose.html')
        else:
            return render_template('rose_bud.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)