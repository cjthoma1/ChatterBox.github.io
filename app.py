from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit, join_room, leave_room

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('welcome')
def handleWelcome(room):
    print('Room Name:' + room)
    join_room(room)


@socketio.on('leaving')
def handleDisconnect(user):
    print('Buh Bye ' + user)
    emit('goodbye', user, broadcast=True)

@socketio.on('show_room')
def handleChatOpen(room, user):
    print('Welcome to:' + room)
    # join_room(room)
    emit('send_chat', room)
    emit('handle_chatObj',user, room=room)
    # emit('join', user + " "+ "has joined", room=room)

# @socketio.on('save_chats')
# def handleChatSave(user, chatName):
#     print('Handling chat save '+ user)
#     emit('handle_chatObj', chatName, room=user)

@socketio.on('logout')
def handleGoodBye(room, user):
    print (user + " is leaving " + room)
    emit('left', user + " "+ "has left", room=room)
    leave_room(room)

@socketio.on('my_event')
def handleConnetion(message):
    print('Statement: ' + message)
    emit('my_response', message, broadcast=True)

@socketio.on('chat')
def handlePrivateChat(message, room, user):
    print('Are we talking?: ' + message + ' '+ room)
    emit('lets_talk', user + ': ' + message, room=room)

@socketio.on('message')
def handleMessage(messages, room):
    for chat in messages:
        emit('my_response', chat, room=room)

@socketio.on('login')
def handleName(users):
    for name in users:
        emit('new_user', name, broadcast=True)

@socketio.on('primary_user')
def handlePrimaryUser(prime):
    emit('primary_user', prime)

if __name__ == '__main__':
    socketio.run(app)
