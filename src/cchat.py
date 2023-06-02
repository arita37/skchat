# -*- coding: utf-8 -*-
"""
   Put your passwords in ENV variables
      ('skype_user', 'user')
      ('skype_pass', 'pass')

   pip install py38.txt
   pip install fire

   ######## Start in shell scriupt
   run_skype.sh 
   
   export skype_user="yourName"
   export skype_pass="yourpass"
   export skype_chatid="thebingChatID"   
   cd src/
   python server.py run_server  --port 12345


   # python server.py test




pip install EdgeGPT --upgrade

"""
import fire, os
from flask import Flask, request
from skpy import Skype, SkypeAuthException, SkypeApiException, SkypeEventLoop
from getpass import getpass
import time
from utilmy import (log, os_makedirs, glob_glob, date_now, json_load, json_save

) 



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
    log(m0)


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
    log('start')
    sk.loop()

#######################################################################################
########## utils ######################################################################
class MySkype(SkypeEventLoop):
    def onEvent(self, event):
        log(repr(event))


def skype_init():
   # Initialize Skype object with your credentials
   global sk 
   sk = Skype(user1, pass1)





#########################################################################################
import asyncio, os
from EdgeGPT import Chatbot, ConversationStyle
import json
from colorama import init as colorama_init
from colorama import Fore, Style



def run_chat():
   """
       python cchat.py run_chat 
       pip install EdgeGPT --upgrade

   """
   colorama_init()
   asyncio.run(main())



def json_update(ddict, dirout=None):

  dirout = os.path.abspath(dirout)
  try :
     d0 = json_load(dirout +"/chathisto.json")
     if d0 is None or 'histo' not in d0:
        d0 = {'histo': []}

     d0['histo'].append(ddict)
     json_save(d0, dirout +"/chathisto.json" )
  except Exception as e :
     log('cannot update chathisto.json', e)


async def main(dirsave="histo/"):       
       ymd = date_now(fmt="%Y%m%d")
       ym  = date_now(fmt="%Y%m")
       dirout = f"{dirsave}/{ym}/{ymd}/"
       os_makedirs(dirout)

       bot = await Chatbot.create(cookies=json_load("cookies.json") if os.path.exists("cookies.json") else None)
       log("Send qq  to exit!")
       while True:
           log("--------------------------------------------")
           iput = input(f"{Fore.GREEN}#Me:{Style.RESET_ALL} ")
           if iput.lower() in ["qq", "exit","quit"]:
               await bot.close()
               log(f"{Fore.BLUE}#GPT:{Style.RESET_ALL} message me again when needed")
               return None 

           log("-----waiting------")    
           result = await bot.ask(prompt=iput, conversation_style=ConversationStyle.creative)
           if result["item"]["result"]["value"] == "Success":
               msg = result["item"]["messages"][-1]["text"]
               log(f"{Fore.RED}#Bard:{Style.RESET_ALL}",  f"{Fore.RED}{msg}{Style.RESET_ALL}" )

               ymhs = date_now(fmt='%Y%m%d-%H:%M:%S')
               json_update({'dt':ymhs   , 'in': iput, 'out': msg}, dirout=dirout)
           else:
               log(f"{Fore.RED}Error occured!{Style.RESET_ALL}")



               
               



##################################################################################################      
from ImageGen import ImageGen
import argparse
import json

async def async_image_gen(args) -> None:
    async with ImageGenAsync(args.U, args.quiet) as image_generator:
        images = await image_generator.get_images(args.prompt)
        await image_generator.save_images(images, output_dir=args.dirout)


def image2(prompt):
   """
       python cchat.py  image --prompt "blue bike in city landscape" --dirout zimg/   --mode 1 


   """
   from EdgeGPT import ImageQuery
   q=ImageQuery("blue bike in city landscape")




def image(cookie_file=None, prompt="bike in black", dirout="ztmp/", mode='async', quiet=1):
    """
       python cchat.py  image --prompt "blue bike in city landscape" --dirout zimg/   --mode 1 

    """
    from utilmy import os_makedirs 
    from box import Box
    args = Box({})

    args.cookie_file = None 
    args.asyncio     = True if mode =='async' else False 
    args.U = None
    args.quiet = True if quiet == 1 else False

    args.prompt = prompt
    args.dirout = dirout 

    os_makedirs(dirout)
   

    # # Load auth cookie
    # with open(args.cookie_file, encoding="utf-8") as file:
    #     cookie_json = json.load(file)
    #     for cookie in cookie_json:
    #         if cookie.get("name") == "_U":
    #             args.U = cookie.get("value")
    #             break

    # if args.U is None:
    #     raise Exception("Could not find auth cookie")

    if not args.asyncio:
        # Create image generator
        image_generator = ImageGen(args.U, args.quiet)
        image_generator.save_images(
            image_generator.get_images(args.prompt),
            output_dir=args.dirout,
        )
    else:
        asyncio.run(async_image_gen(args))


#######################################################################################
if __name__ == '__main__':
    fire.Fire()

