# -*- coding: utf-8 -*-
"""
   Put your passwords in ENV variables
      ('skype_user', 'user')
      ('skype_pass', 'pass')

   pip install py38.txt
   pip install fire

   ######## Start
   python server.py run_server  --port 12345

   python server.py test



"""
import fire, os
from flask import Flask, request
from skpy import Skype, SkypeAuthException, SkypeApiException, SkypeEventLoop
from getpass import getpass
import time


########################################################################3########
global user1, pass1, bingchat, sk, app
user1 = os.environ.get('skype_user', 'user')
pass1 = os.environ.get('skype_pass', 'pass')
basid = os.environ.get('skype_chatid', 'someid')


################################################################################
def test():
    chatid=""
    sk = Skype(user1, pass1) # connect to Skype
    ch = sk.chats[chatid]
    txt= "ok"
    ch.sendMsg(txt) # plain-text message
    time.sleep(8)
    mlist= ch.getMsgs() # retrieve recent message
    m0 = mlist[0].markup
    print(m0)


##############################################################################

app = Flask(__name__)

@app.route('/sendmsg', methods=['POST'])
def send_message():
    """
    method query = POST

    Receives a json via http/https with the message text 
    (the `text` field) and who to send it to with the 
    `recipient` field
    """
    try:
        data = request.json
        text = data.get('text')
        recipient = data.get('recipient')
        
        # Send message
        ch = sk.contacts[recipient].chat
        ch.sendMsg(text)
        return 'Message sent successfully'
    except (SkypeAuthException, SkypeApiException) as e:
        return str(e), 401

@app.route('/getmsg', methods=['GET'])
def get_messages():
    """
    We accept all messages
    """
    try:
        messages = []
        for chat_id in sk.chats.recent():
            try:
                chat = sk.chats[chat_id]
                for msg in chat.getMsgs(): 
                    messages.append({'sender': msg.userId,
                                    'text': msg.content})
            except: 
                pass
        return {'messages': messages}
    except (SkypeAuthException, SkypeApiException) as e:
        return str(e), 401
 
def run_server(port=12354):
    skype_init() 
    app.run(port=port)


#######################################################################################

def run_loop_event():
    sk = MySkype(user1, pass1, autoAck=True)
    sk.subscribePresence() # Only if you need contact presence events.
    print('start')
    sk.loop()

#######################################################################################
########## utils ######################################################################
class MySkype(SkypeEventLoop):
    def onEvent(self, event):
        print(repr(event))


def skype_init():
   # Initialize Skype object with your credentials
   global sk 
   sk = Skype(user1, pass1)



#######################################################################################
if __name__ == '__main__':
    fire.Fire()



