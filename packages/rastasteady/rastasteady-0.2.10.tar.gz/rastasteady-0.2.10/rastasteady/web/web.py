#!/usr/bin/env python
# coding=utf-8

# based on https://gist.github.com/dAnjou/2874714

from flask import Flask, flash, render_template, request
from werkzeug.utils import secure_filename
from rastasteady.rastasteady import RastaSteady
import os

DEBUG = os.environ.get('DEBUG', True)
PORT = os.environ.get('PORT', 8080)
UPLOAD_FOLDER = ''
ALLOWED_EXTENSIONS = set(['mp4', 'txt'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'djistabilizationsoftware'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route("/")
def index():
    return render_template('index.html', title='RastaSteady')

@app.route('/upload', methods = ['POST'])
def upload_file():
    file = request.files['file']
    if file and allowed_file(file.filename):
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename)))
        flash('Video subido correctamente')

        myVideo = RastaSteady(file.filename)
        myVideo.stabilize()
        myVideo.rastaview()
        myVideo.dual()
    else:
        flash('Video no enviado correctamente o extensión invalida')

    return render_template('index.html', title='RastaSteady')
     
def web():
    app.run(host='0.0.0.0', port=PORT, debug=DEBUG)

if __name__ == '__main__':
    web()
