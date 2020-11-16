import numpy as np
from flask import Flask

from inference_core import inference_engine
inference_instance = inference_engine()
from utility import decode_image, stringify

app = Flask(__name__)

@app.route('/')
def homepage():
    a = np.zeros((2,3))
    print(a)
    return 'From docker container'

def test_flask():
    app.run(debug=True, host='0.0.0.0')

def test_inference():
    img_path = "grey_whale.jpeg"
    img = decode_image(img_path)
    prediction = inference_instance.get_class_probabilities(img, top_k=5)
    output = stringify(prediction)
    print(output)


if __name__ == '__main__':
    # test_flask()
    # test_inference()
    pass