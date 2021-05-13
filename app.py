from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, join_room, leave_room, emit
# from flask_Sesstion import Session
import eventlet
eventlet.monkey_patch()

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'secret'
app.config['SESSION_TYPE'] = 'filesystem'

# Session(app)

TempUser = []
TempRoom = []

socket = SocketIO(app,manage_session=False)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if(request.method=='POST'):
        username = request.form['username']
        room = request.form['room']
        #Store the data in session
        session['username'] = username
        session['room'] = room
        return render_template('chat.html', session = session)
    else:
        if(session.get('username') is not None):
            return render_template('chat.html', session = session)
        else:
            return redirect(url_for('index'))

@socket.on('join',namespace='/chat')
def join(message):
    room = session.get('room')
    join_room(room)
    emit('status', {'msg': session.get('username') +' has entered the room.'}, room=room)

@socket.on('text',namespace='/chat')
def text(message):
    room = session.get('room')
    emit('message', {'msg': session.get('username') + ' : ' + message['msg']}, room=room)


@socket.on('left',namespace='/chat')
def left(message):
    room = session.get('room')
    username = session.get('username')
    leave_room(room)
    session.clear()
    emit('status', {'msg': username + ' has left the room.'}, room=room)

if __name__ == '__main__':
    #app.run()

    socket.run(app)

    #eventlet.wsgi.server(eventlet.listen(('', 5000)), app,log_output=False)