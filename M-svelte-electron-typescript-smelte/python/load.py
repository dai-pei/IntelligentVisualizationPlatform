import librosa
from flask import Flask,make_response
from flask_restful import request,Api
import json

app = Flask(__name__)
api = Api(app) 

def LoadData(filepath):
    y,sr=librosa.load(filepath)
    # print(y)
    # print(sr)

    ret=tuple(y.tolist())
    
    # print(ret)
    return y

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
        return json.dumps({"loaddata":LoadData(filep).tolist()})
    return {"msg":"fail"}

@app.route('/spectrum/', methods=['POST', 'GET'])
def spectrum():
    error = None
    if request.method == 'POST':
        print(request.form['name'])
    return {"msg":"success"}

if __name__ == '__main__':    
    app.run(debug=True,port=6005)