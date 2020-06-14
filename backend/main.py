import os
from flask import Flask, request, redirect, url_for, render_template, jsonify, send_file
from werkzeug.utils import secure_filename
from flask_cors import CORS, cross_origin
import uuid
import measure
import base64
import numpy as np
import cv2
import io


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'heic'}
app = Flask(__name__)
cors = CORS(app)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods = ['POST'])
@cross_origin()
def upload_file():
    if request.method == 'POST':
        if 'image' not in request.files:
            return 'No file part'
        file = request.files['image']
        if file.filename == '':
            return 'no file there mate'
        if file and allowed_file(file.filename):
            ft = file.filename.split('.')[1]
            fn = '{}.{}'.format(uuid.uuid4().hex, ft)
            file_path = 'images/{}'.format(fn)
            file.save(file_path)
            data, path = measure.runner(fn)
            os.remove('images/{}'.format(path))
            return jsonify(data)


if __name__ == '__main__':
    app.run(debug = True, threaded=False)
