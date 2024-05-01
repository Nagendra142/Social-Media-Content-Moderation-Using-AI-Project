from flask import Flask, render_template,request,redirect
from flask_socketio import SocketIO
from moderationCode import *
from admin import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
socketio = SocketIO(app)

@app.route('/')
def sessions():
    
    return render_template('session.html')

@app.route('/badwords')
def badwords():
    return render_template('index.html')

@app.route('/addBadWordForm',methods=['POST'])
def addBadWordForm():
    message=request.form['message']
    # admin database
    addBadWord(message)
    #direct
    # AddData(message)
    return render_template('index.html',err='Bad Message Added')

# @app.route('/addBadWordAdmin',methods=['post'])
# def addBadWordAdmin():
#     message=request.form['message']
#     # admin database
#     addBadWord(message)
#     #direct
#     # AddData(message)
#     return redirect('/admin')

@app.route('/accept',methods=['POST'])
def acceptTheData():
    value=request.form['message']
    #adding to dataset
    AddData(value)
    print(value)
    #delete the message from db
    fetchedData=Delete(value)
    return redirect('/admin')
    # return render_template('admin.html',data=fetchedData,Message="The Data is Added to Dataset Successfully") 

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/logout')
def logout():
    return render_template('session.html')


@app.route('/validate',methods=['POST'])
def valdiate():
    username=request.form['username']
    password=request.form['password']
    if(username=='admin' and password=='Nagendra'):
        return redirect('/admin')
    else:
        return render_template('login.html',err='Invalid Credentials')

@app.route('/reject',methods=['POST'])
def rejectTheData():
    value=request.form['message']
    print(value)
    #delete the message from db
    fetchedData=Delete(value)
    return redirect('/admin')
    # return render_template('admin.html',data=fetchedData,Message="The Data is rejected and removed from ADMIN DATA")     

def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')

@app.route('/admin')
def adminPage():
    fetchedData=adminData() 
    return render_template('admin.html',data=fetchedData)
@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print('received my event: ' + str(json))
    print(json['message'])
    if True:
        status=passMessage(json['message'])
        if status==True:
            socketio.emit('my response', json, callback=messageReceived)
        if status==False:
            socketio.emit('badword alert',"Bad Word Detected",callback=messageReceived)
    # except:
    #     print ('hi')
    #     pass

if __name__ == '__main__':
    socketio.run(app, host='127.0.0.1', debug=True,port=6001)