import librosa
import numpy as np
from flask import Flask,make_response
from flask_restful import request,Api
import json

app = Flask(__name__)
api = Api(app) 

def LoadOrgData(filepath):
    y,sr=librosa.load(filepath)
    return y

def LoadSpecData(filepath):
    y,sr=librosa.load(filepath)
    S = np.abs(librosa.stft(y,n_fft=2048,window='hann'))
    S_db=librosa.power_to_db(S ** 2)
    return S_db

@app.route('/', methods=['POST', 'GET'])
def root():
    return {"msg":"success"}


@app.route('/orgdata/', methods=['POST', 'GET'])
def orgdata():
    if request.method == 'POST':
        print(request.json)
        filep=request.json['filepath']
        print(filep)
        # res = make_response()
        # res.data = json.dumps({"loaddata":LoadData(filep).tolist()})
        return json.dumps({"loaddata":LoadOrgData(filep).tolist()})
    return {"msg":"fail"}

@app.route('/spectrum/', methods=['POST', 'GET'])
def spectrum():
    error=None
    if request.method == 'POST':
        filep=request.json['filepath']
        print(filep)
        return json.dumps({"loaddata":LoadSpecData(filep).tolist()})
    return {"msg":"fail"}

if __name__ == '__main__':    
    app.run(debug=True,port=6005)