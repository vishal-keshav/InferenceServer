import numpy as np
from flask import Flask

app = Flask(__name__)

@app.route('/')
def homepage():
    a = np.zeros((2,3))
    print(a)
    return 'From docker container'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')