import os
from werkzeug.utils import secure_filename

from flask import Flask, render_template, request, jsonify

import json

from utility import decode_image, stringify
from inference_core import inference_engine


inference_instance = inference_engine()

UPLOAD_FOLDER = os.getcwd() + '/upload'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


# app = Flask(__name__, static_url_path='')
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

basedir = os.path.abspath(os.path.dirname(__file__))

def allowed_file(filename):
    """
    Checks to make sure sent image has a valid filetype
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[-1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    """
    Serves the index.html
    """
    return render_template('index.html')

# Sample command to POST request to this route:
# curl -X POST -F "file=@cat.jpg" http://0.0.0.0:5000/uploadajax
@app.route('/uploadajax', methods=["GET", "POST"])
def uploadfile():
    if request.method == 'POST':
        files = request.files['file']
        print(files.filename, flush=True)
        # check validity of file
        if files and allowed_file(files.filename):
            filename = secure_filename(files.filename)
            print(filename, flush=True)
            updir = os.path.join(basedir, 'upload/')
            image_path = os.path.join(updir, filename)
            files.save(image_path)
            file_size = os.path.getsize(os.path.join(updir, filename))
        else:
            app.logger.info('ext name error')
            return jsonify(error='ext name error')
        image = decode_image(image_path) # read in the image
        predictions = inference_instance.get_class_probabilities(image)
        return stringify(predictions)

@app.route('/radio_button', methods=["GET", "POST"])
def radio_selection():
    if request.method == 'POST':
        selection = json.loads(request.get_data(as_text=True))['radio_sel']  # converts json byte string to dict
        print(selection)
        image_path = None
        if selection=='1':  #(cat)
            image_path = os.path.join(os.getcwd(), 'static', 'images', 'n02121808_1421_domestic_cat.jpg')
        elif selection=='2':  # (whale)
            image_path = os.path.join(os.getcwd(), 'static', 'images', 'grey_whale.jpeg')
        elif selection=='3':  # (dog)
            image_path = os.path.join(os.getcwd(), 'static', 'images', 'n02084071_1365_dog.jpg')

        image = decode_image(image_path)  # read the image
        predictions = inference_instance.get_class_probabilities(image)
        return stringify(predictions)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
