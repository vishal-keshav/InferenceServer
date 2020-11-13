import flask
from flask import (Flask,
                  render_template,
                  request,
                  jsonify,
                  url_for
                  )
import os
import binascii

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

if __name__ == "__main__":
    app.run()
