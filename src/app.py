import flask
from flask import (Flask,
                  render_template,
                  request,
                  jsonify,
                  url_for
                  )
import os
import binascii
from werkzeug.utils import secure_filename

import torch
from torchvision import transforms
from PIL import Image
import pandas as pd
import numpy as np

UPLOAD_FOLDER = os.getcwd() + '/upload'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

# you can find images here https://github.com/ajschumacher/imagen/tree/master/imagen
imagenet_data = pd.read_csv(os.path.join(os.getcwd(), 'static', 'imagenet_labels.txt'), sep=' ', names=['tag', 'id', 'name'])
IMAGENET_LABELS = np.array(imagenet_data['name'])

app = Flask(__name__, static_url_path='')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

basedir = os.path.abspath(os.path.dirname(__file__))

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[-1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    """
    Homepage: serve our visualization page, index.html
    """
    return render_template('index.html')

@app.route('/uploadajax', methods=["GET", "POST"])
def uploadfile():
    if request.method == 'POST':
        files = request.files['file']  # see paramName in app.js
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

        prediction = make_prediction(image_path)
        print(prediction)

        return prediction

        # below is old code from my old project but we might want to use this
        # my project ran a CV algorithm on the inputed file and then returned another
        # image as a result which is why it sends an encoded string back to the user
        # we probably just want to send back the classification string

        # result = execute_solver(files)
        #
        # if result == 'good':
        #     with open("static/images/solution.jpg", "rb") as image_file:
        #         encoded_string = binascii.b2a_base64(image_file.read())
        #     return encoded_string
        #
        # elif result == 'error':
        #     print(result)
        #     with open("static/images/error.jpg", "rb") as image_file:
        #         encoded_string = binascii.b2a_base64(image_file.read())
        #     return encoded_string

def preprocess_image(input_image):
    preprocess = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
    input_tensor = preprocess(input_image)
    return input_tensor

def make_prediction(image_path):
    # load densenet121
    model = torch.hub.load('pytorch/vision:v0.6.0', 'densenet121', pretrained=True)
    model.eval()

    # before classifying image needs to be preprocessed
    # https://pytorch.org/hub/pytorch_vision_densenet/
    input_image = Image.open(image_path)

    # apply preprocessing
    input_tensor = preprocess_image(input_image)

    # create a mini-batch
    input_batch = input_tensor.unsqueeze(0)

    # move the input batch and model to GPU for speed if available
    if torch.cuda.is_available():
        input_batch = input_batch.to('cuda')
        model.to('cuda')

    # run model
    with torch.no_grad():
        output = model(input_batch)

    predictions = (torch.nn.functional.softmax(output[0], dim=0)).detach().numpy()  # this normalizes the scores

    top5 = predictions.argsort()[-5:][::-1]
    # top1 = IMAGENET_LABELS[np.argmax(predictions)]
    print(top5)  # get top 5 locations

    prediction_str = ''
    for idx in top5:
        label = IMAGENET_LABELS[idx]
        score = predictions[idx]
        prediction_str+= f'{label}, ({score:.04f})\n'
    print(prediction_str)
    return prediction_str

# User sends request http://127.0.0.1:5000/class?image=giraffe.png
@app.route('/class', methods=['GET'])
def image():
    if 'image' in request.args:
        image = request.args['image']
    else:
        return "Error: No image provided. Please specify an input image."

    # load densenet121
    model = torch.hub.load('pytorch/vision:v0.6.0', 'densenet121', pretrained=True)
    model.eval()

    # before classifying image needs to be preprocessed
    # https://pytorch.org/hub/pytorch_vision_densenet/
    input_image = Image.open(image)

    # apply preprocessing
    input_tensor = preprocess_image(input_image)

    # create a mini-batch
    input_batch = input_tensor.unsqueeze(0)

    # move the input batch and model to GPU for speed if available
    if torch.cuda.is_available():
        input_batch = input_batch.to('cuda')
        model.to('cuda')

    # run model
    with torch.no_grad():
        output = model(input_batch)

    # print (output[0])
    return (output[0])


if __name__ == "__main__":
    app.run()
