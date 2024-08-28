import json
import pickle
from flask import Flask
from flask import request
from flask import app
from flask import jsonify
from flask import url_for
from flask import render_template
import numpy as np
import pandas as pd

app=Flask(__name__)
## Load the model
regmodel=pickle.load(open('models/regmodel.pkl','rb'))
scalar=pickle.load(open('models/scaling.pkl','rb'))
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/predict_api',methods=['POST'])
def predict_api():
    data=request.json['data']
    print(data)
    print(np.array(list(data.values())).reshape(1,-1))
    new_data=scalar.transform(np.array(list(data.values())).reshape(1,-1))
    output=regmodel.predict(new_data)
    print(output[0])
    return jsonify(output[0])

@app.route('/predict',methods=['POST'])
def predict():
    data=[float(x) for x in request.form.values()]
    final_input=scalar.transform(np.array(data).reshape(1,-1))
    print(final_input)
    output = f"{regmodel.predict(final_input)[0]:.2f}"
    return render_template("home.html",prediction_text="The House price prediction is {}".format(output))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)