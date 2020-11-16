import os
from werkzeug.utils import secure_filename

from flask import Flask, render_template, request, jsonify

import json

from utility import decode_image, stringify
from inference_core import inference_engine
inference_instance = inference_engine()


UPLOAD_FOLDER = os.getcwd() + '/upload'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


# load densenet121, initialized here so that it isn't constantly reset each function.
MODEL = torch.hub.load('pytorch/vision:v0.6.0', 'densenet121', pretrained=True)
MODEL.eval()

# app = Flask(__name__, static_url_path='')
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



basedir = os.path.abspath(os.path.dirname(__file__))

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[-1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    """
    Serves the index.html
    """
    return render_template('index.html')

@app.route('/uploadajax', methods=["GET", "POST"])
def uploadfile():
    if request.method == 'POST':
        files = request.files['file']
        print(files.filename, flush=True)
        if files and allowed_file(files.filename):
            filename = secure_filename(files.filename)  # see this for what this is doing https://flask.palletsprojects.com/en/1.1.x/patterns/fileuploads/
            print(filename, flush=True)
            updir = os.path.join(basedir, 'upload/')
            image_path = os.path.join(updir, filename)
            files.save(image_path)
            file_size = os.path.getsize(os.path.join(updir, filename))
        else:
            app.logger.info('ext name error')
            return jsonify(error='ext name error')

        image = decode_image(image_path)
        predictions = inference_instance.get_class_probabilities(image)
        return stringify(predictions)

@app.route('/radio_button', methods=["GET", "POST"])
def radio_selection():
    if request.method == 'POST':
        selection = json.loads(request.get_data(as_text=True))['radio_sel']  # converts json byte string to dict
        print(selection)
        if selection=='1':  #(cat)
            image_path = os.path.join(os.getcwd(), 'static', 'images', 'n02121808_1421_domestic_cat.jpg')
        elif selection=='2':  # (whale)
            image_path = os.path.join(os.getcwd(), 'static', 'images', 'grey_whale.jpeg')
        elif selection=='3':  # (dog)
            image_path = os.path.join(os.getcwd(), 'static', 'images', 'n02084071_1365_dog.jpg')

        prediction = make_prediction(image_path)
        print(prediction)

        return prediction


# User sends request http://127.0.0.1:5000/class?image=giraffe.png
@app.route('/class', methods=['GET'])
def image():
    if 'image' in request.args:
        image_path = request.args['image']
    else:
        return "Error: No image provided. Please specify an input image."
    
    image = decode_image(image_path)
    predictions = inference_instance.get_class_probabilities(image)
    return stringify(predictions)

@app.route('/')
def test():
    return "This is a test route"

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
