import librosa
import numpy as np
from flask import Flask,make_response
from flask_restful import request,Api
import json

app = Flask(__name__)
api = Api(app) 

def findTimeIndex(times,second):
    prevEle=0
    secondIdx=-1
    # print(second.type)
    # print(second)
    second=float(second)
    for idx,ele in enumerate(times):
        # print(idx)
        # print(ele)
        if prevEle<=second and ele>=second:
            secondIdx=idx
            break
        prevEle=ele
    # print(secondIdx)
    return secondIdx

def LoadOrgData(filepath,startsecond,endsecond):
    y,sr=librosa.load(filepath)
    samples = librosa.samples_like(y,hop_length=1)
    # print('samples = %s'%samples)
    times = librosa.frames_to_time(samples,sr=sr,hop_length=1)
    # print('times = %s'%times)
    startIdx=findTimeIndex(times,startsecond)
    endIdx=findTimeIndex(times,endsecond)
    print("start idx",startIdx)
    print("end idx",endIdx)
    
    ret=y[startIdx:endIdx]
    print(ret.shape)
    return ret
    # 健壮性处理，如果startSec或者endSec超出了歌曲范围（不允许）

def LoadSpecData(filepath):
    print("load spec data: ",filepath)
    y,sr=librosa.load(filepath)
    y=y[:250000]
    S = np.abs(librosa.stft(y,n_fft=2048,window='hann'))
    S_db=librosa.power_to_db(S ** 2)
    return S_db

def LoadZeroCrossingRate(filepath,startsecond,endsecond):
    y=LoadOrgData(filepath,startsecond,endsecond)
    # zcrs = librosa.feature.zero_crossing_rate(y=y,frame_length=2048, hop_length=512, center=True)
    zcrs = librosa.feature.zero_crossing_rate(y)
    print(zcrs.shape)
    return zcrs[0]

def LoadSpectrumCentroid(filepath,startsecond,endsecond):
    y=LoadOrgData(filepath,startsecond,endsecond)
    cent = librosa.feature.zero_crossing_rate(y)
    print(cent.shape)
    return cent[0]

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
        startsec=request.json['startsecond']
        endsec=request.json['endsecond']
        # print(filep,startsec,endsec)
        ret=json.dumps({"loaddata":LoadOrgData(filep,startsec,endsec).tolist()})
        # print(LoadOrgData(filep,startsec,endsec).shape)
        return ret
    return {"msg":"fail"}

@app.route('/spectrum/', methods=['POST', 'GET'])
def spectrum():
    error=None
    if request.method == 'POST':
        filep=request.json['filepath']
        print(filep)
        return json.dumps({"loaddata":LoadSpecData(filep).tolist()})
    return {"msg":"fail"}

@app.route('/zerocrossingrate/', methods=['POST', 'GET'])
def zerocrossingrate():
    error=None
    if request.method == 'POST':
        filep=request.json['filepath']
        startsec=request.json['startsecond']
        endsec=request.json['endsecond']
        print(filep,startsec,endsec)
        ret= json.dumps({"zcrs":LoadZeroCrossingRate(filep,startsec,endsec).tolist()})
        # print(ret)
        return ret
    return {"msg":"fail"}

@app.route('/spectrumcentroid/', methods=['POST', 'GET'])
def spectrumcentroid():
    error=None
    if request.method == 'POST':
        filep=request.json['filepath']
        startsec=request.json['startsecond']
        endsec=request.json['endsecond']
        print(filep,startsec,endsec)
        ret= json.dumps({"cent":LoadSpectrumCentroid(filep,startsec,endsec).tolist()})
        # print(ret)
        return ret
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

    