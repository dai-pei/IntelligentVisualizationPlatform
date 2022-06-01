import librosa
import numpy as np
from flask import Flask,make_response
from flask_restful import request,Api
import json

app = Flask(__name__)
api = Api(app) 

generateAudioIdx=0

def GetDuration(filepath,startsec=-1,endsec=-1):
    y,sr=librosa.load(filepath)
    if(startsec==-1 or endsec==-1):
        return librosa.get_duration(y,sr)
    return 1000000
    
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

def LoadOrgDataFulllLength(filepath):
    y,sr=librosa.load(filepath)
    return y

def LoadSpecData(filepath):
    print("load spec data: ",filepath)
    y,sr=librosa.load(filepath)
    # y=y[:250000]
    S = np.abs(librosa.stft(y,n_fft=2048,window='hann'))
    S_db=librosa.power_to_db(S ** 2)
    # S = np.abs(librosa.stft(y,n_fft=1024,window='hann'))
    # return S    
    return S_db

def GenerateAudioFromSamples(data,samplerate):
    global generateAudioIdx
    path="Audio"+str(generateAudioIdx)+".wav"
    audiodata=np.asfortranarray(data)
    librosa.output.write_wav(path,audiodata, sr=samplerate)
    generateAudioIdx+=1
    return path

def LoadZeroCrossingRate(filepath,startsecond=-1,endsecond=-1):
    # y=LoadOrgData(filepath,startsecond,endsecond)
    y=LoadOrgDataFulllLength(filepath)
    # zcrs = librosa.feature.zero_crossing_rate(y=y,frame_length=2048, hop_length=512, center=True)
    zcrs = librosa.feature.zero_crossing_rate(y)
    zcrsMax=np.max(zcrs[0])
    print(zcrs.shape)
    return zcrs[0],zcrsMax

def LoadSpectrumCentroid(filepath,startsecond=-1,endsecond=-1):
    # y=LoadOrgData(filepath,startsecond,endsecond)
    y=LoadOrgDataFulllLength(filepath)
    cent = librosa.feature.spectral_centroid(y)
    # print(cent.shape)
    centmax=np.max(cent[0])
    return cent[0],centmax

def LoadFeaturesForKNN(filepathmul,classes,feature1,feature2):
    N_FFT=1024
    retArr=[]
    ret1max=-10000
    ret1min=10000
    ret2max=-10000
    ret2min=10000
    for filepathinfo in filepathmul:
        y=LoadOrgDataFulllLength(filepathinfo[0])
        label=filepathinfo[1]
        if feature1=='zero':
            zero=librosa.feature.zero_crossing_rate(y)
            ret1=np.max(zero[0])
            ret1max=max(ret1max,ret1)
            ret1min=min(ret1min,ret1)
        elif feature1=='cent':
            cent = librosa.feature.spectral_centroid(y)
            ret1=np.max(cent[0])
            ret1max=max(ret1max,ret1)
            ret1min=min(ret1min,ret1)
        elif feature1=='mfcc':
            mfcc=librosa.feature.mfcc(y,n_mfcc=20, dct_type=2,norm='ortho',n_fft=N_FFT,hop_length=int(N_FFT/4))
            ret1=np.max(mfcc[0])
            ret1max=max(ret1max,ret1)
            ret1min=min(ret1min,ret1)

        if feature2=='zero':
            zero=librosa.feature.zero_crossing_rate(y)
            ret2=np.max(zero[0])
            ret3=np.float64(ret2).item()
            ret2max=max(ret2max,ret3)
            ret2min=min(ret2min,ret3)
        elif feature2=='cent':
            cent = librosa.feature.spectral_centroid(y)
            ret2=np.max(cent[0])
            ret3=np.float64(ret2).item()
            ret2max=max(ret2max,ret3)
            ret2min=min(ret2min,ret3)
        elif feature2=='mfcc':
            mfcc=librosa.feature.mfcc(y,n_mfcc=20, dct_type=2,norm='ortho',n_fft=N_FFT,hop_length=int(N_FFT/4))
            ret2=np.max(mfcc[0])
            ret3=np.float64(ret2).item()
            ret2max=max(ret2max,ret3)
            ret2min=min(ret2min,ret3)

        tempArr=[]
        # print(type(ret1))
        # print(type(ret3))
        # 不知道为什么直接使用ret2的话，由于type(ret2)为float32，无法在json.dumps()中
        # 被转换，所以需要做一次预处理，把float32转成np.float64/python float
        tempArr.append(ret1)
        tempArr.append(ret3)
        tempArr.append(label)
        retArr.append(tempArr)

    # print(retArr)
    return retArr,ret1max,ret1min,ret2max,ret2min

@app.route('/', methods=['POST', 'GET'])
def root():
    return {"msg":"success"}

@app.route('/duration/', methods=['POST', 'GET'])
def duration():
    error=None
    if request.method == 'POST':
        filep=request.json['filepath']
        return json.dumps({"duration":GetDuration(filep)})
    return {"msg":"fail"}

@app.route('/orgdata/', methods=['POST', 'GET'])
def orgdata():
    if request.method == 'POST':
        print(request.json)
        filep=request.json['filepath']
        print("filep is ",filep)
        # startsec=request.json['startsecond']
        # endsec=request.json['endsecond']
        # print(filep,startsec,endsec)
        ret=json.dumps({"duration":GetDuration(filep),"orgdata":LoadOrgDataFulllLength(filep).tolist()})
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
        # startsec=request.json['startsecond']
        # endsec=request.json['endsecond']
        # print(filep,startsec,endsec)
        zero=LoadZeroCrossingRate(filep)
        ret= json.dumps({"zcrs":zero[0].tolist(),"zcrsmax":zero[1]})
        return ret
    return {"msg":"fail"}

@app.route('/spectrumcentroid/', methods=['POST', 'GET'])
def spectrumcentroid():
    error=None
    if request.method == 'POST':
        filep=request.json['filepath']
        # startsec=request.json['startsecond']
        # endsec=request.json['endsecond']
        # print(filep,startsec,endsec)
        cent=LoadSpectrumCentroid(filep)
        ret= json.dumps({"cent":cent[0].tolist(),"centmax":cent[1]})
        # print(ret)
        return ret
    return {"msg":"fail"}

@app.route('/featuresforknn/', methods=['POST', 'GET'])
def featuresforknn():
    error=None
    if request.method == 'POST':
        filepathmul=request.json['filepathmulti']
        classes=request.json['classes']
        feature1=request.json['feature1']
        feature2=request.json['feature2']
        # print(filepathmul,classes,feature1,feature2)
        retArr= LoadFeaturesForKNN(filepathmul,classes,feature1,feature2)
        # print(type(retArr))
        # print(retArr)
        ret= json.dumps({"featuresforknn":retArr[0],"ret1max":retArr[1],
        "ret1min":retArr[2],
        "ret2max":retArr[3],
        "ret2min":retArr[4],})
        return ret
    return {"msg":"fail"}

@app.route('/generateaudiofromsamples/', methods=['POST', 'GET'])
def generateaudiofromsamples():
    error=None
    if request.method == 'POST':
        data=request.json['wavedata']
        samplerate=request.json['samplerate']
        # print(filepathmul,classes,feature1,feature2)
        retArr= GenerateAudioFromSamples(data,samplerate)
        # print(type(retArr))
        # print(retArr)
        ret= json.dumps({"path":retArr})
        return ret
    return {"msg":"fail"}

if __name__ == '__main__':    
    app.run(debug=True,port=6005)  