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
    y=y[:250000]
    S = np.abs(librosa.stft(y,n_fft=2048,window='hann'))
    S_db=librosa.power_to_db(S ** 2)
    return S_db

def LoadZeroCrossingRate(filepath):
    y,sr=librosa.load(filepath)
    # y=y[:250000]
    zcrs = librosa.feature.zero_crossing_rate(x)
    print(zcrs.shape)
    return zcrs

def GetDuration(filepath,startsec=-1,endsec=-1):
    y,sr=librosa.load(filepath)
    if(startsec==-1 or endsec==-1):
        return librosa.get_duration(y,sr)
    return 1000000
    

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

@app.route('/zerocrossing/', methods=['POST', 'GET'])
def zerocrossing():
    error=None
    if request.method == 'POST':
        filep=request.json['filepath']
        print(filep)
        return json.dumps({"loaddata":LoadZeroCrossingRate(filep).tolist()})
    return {"msg":"fail"}

@app.route('/duration2/', methods=['POST', 'GET'])
def duration2():
    error=None
    if request.method == 'POST':
        filep=request.json['filepath']
        startsec=request.json['startsecond']
        endsec=request.json['endsecond']
        return json.dumps({"duration":GetDuration(filep,startsec,endsec).tolist()})
    return {"msg":"fail"}

@app.route('/duration/', methods=['POST', 'GET'])
def duration():
    error=None
    if request.method == 'POST':
        filep=request.json['filepath']
        return json.dumps({"duration":GetDuration(filep)})
    return {"msg":"fail"}

if __name__ == '__main__':    
    app.run(debug=True,port=6005)

    