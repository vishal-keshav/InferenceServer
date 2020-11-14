import flask
from flask import (Flask,
                  render_template,
                  request,
                  jsonify,
                  url_for
                  )
import os
import binascii

import torch
from torchvision import transforms
from PIL import Image


UPLOAD_FOLDER = '/upload'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

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
def upldfile():
    if request.method == 'POST':
        files = request.files['file']
        print(files.filename)
        print('bad dog')
        if files and allowed_file(files.filename):
            filename = secure_filename(files.filename)
            print(filename)
            updir = os.path.join(basedir, 'upload/')
            files.save(os.path.join(updir, filename))
            file_size = os.path.getsize(os.path.join(updir, filename))
        else:
            app.logger.info('ext name error')
            return jsonify(error='ext name error')

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
    preprocess = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
    input_tensor = preprocess(input_image)

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
