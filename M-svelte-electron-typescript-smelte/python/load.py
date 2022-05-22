import librosa
from flask import Flask
from flask_restful import Resource, Api 

app = Flask(__name__)
api = Api(app) 
# class HelloWorld(Resource):    
#     def get(self):        
#         # y,sr=librosa.load("C:/Users/D/Desktop/test.wav")
#         return {'hello': 'world'} 

#     def post(self):
#         print(request.headers)
#         print(request.stream.read())
#         return 'welcome'

# api.add_resource(HelloWorld, '/')
@app.route('/')
def hello_world():
    return {'hello': 'world'}

@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        if valid_login(request.form['username'],
                       request.form['password']):
            return log_the_user_in(request.form['username'])
        else:
            error = 'Invalid username/password'
    # the code below this is executed if the request method
    # was GET or the credentials were invalid
    return 'noerror'

if __name__ == '__main__':    
    app.run(debug=True,port=6005)