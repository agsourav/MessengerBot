import os, sys
from flask import Flask, request
from pymessenger.bot import Bot
from utils import wit_handleMessage, wit_postback
import sqlite3
app = Flask(__name__)

conn = sqlite3.connect('bookyourshow.db')
c = conn.cursor()

PAGE_ACCESS_TOKEN = "EAASQychkTOsBAK4P1zC5Ax3XHQWtVNWAU5oTqpJBo3tvMmO0rMPCzFXwG3OTXjoxoRrc9djUx44cDLLj4dR336ZCzeKMNenqwN5KzXaZAXKdQco0wJZBBVxyJbFGNBmChdqfZCUsb7CZBimUfNUJStrAf41UoXEJoiHY6PZC2kt0w27qWg44gh"
bot = Bot(PAGE_ACCESS_TOKEN)
URL = "https://graph.facebook.com/v2.6/me/100885468177987"
@app.route('/', methods=['GET'])

def verify():
	if request.args.get("hub.mode")=="subscribe" and request.args.get("hub.challenge"):
		if not request.args.get("hub.verify_token")=="hello":
			return "Verification token mismatch", 403
		return request.args["hub.challenge"], 200
	return "Hello world", 200

@app.route('/', methods = ['POST'])
def webhook():
                             
        data = request.get_json()
        log(data)

        if data['object'] == 'page':
                for entry in data['entry']:
                        #log(entry)
                        webhook_event = entry['messaging'][0]
                        sender_id = webhook_event['sender']['id']
                        recipient_id = webhook_event['recipient']['id']
                        log(webhook_event)
                        if 'message' in webhook_event:
                                req = wit_handleMessage(sender_id,webhook_event['message'])
                                log(req)
                                bot.send_message(sender_id, req)
                        if 'postback' in webhook_event:
                                log(webhook_event)
                                #bot.send_message(sender_id, {'text':'postback request'})
                                req = wit_postback(sender_id, webhook_event['postback'])
                                if not req:
                                        req = {'text':'Value error'}
                                bot.send_message(sender_id, req)
                                
        return "ok", 200
                                
        
"""
        if data['object'] == 'page':
                for entry in data['entry']:
                        for messaging_event in entry['messaging']:
                                #IDs
                                sender_id = messaging_event['sender']['id']
                                recipient_id = messaging_event['recipient']['id']

                                #response = get_started()
                                #k = bot.send_text_message(sender_id, response)
                                #print("getting started:",k)
                                if messaging_event.get('message'):
                                        if 'text' in messaging_event['message']:
                                                messaging_text = messaging_event['message']['text']
                                        else:
                                                messaging_text = 'no text'
                                        print(messaging_text)
                                        #Echo
                                        response = None

                                        category = wit_response(messaging_text)
                                        print(category)
                                        for entity in category:
                                        #response = view_events()
                                                if entity =="greet":
                                                        response = greetings(messaging_text, recipient_id)
                                                        print('\n',response)
                                                        bot.send_quick_reply(sender_id, response)
                                                        
                                                elif entity == "eventtype":
                                                        val = category[entity]
                                                        bot.send_text_message(sender_id, val)

                                                elif entity == "querytype":
                                                        val = category[entity]
                                                        if val=="events":
                                                                response = view_event()
                                                        elif val=="bookings":
                                                                response = view_bookings('bot')
                                                        bot.send_generic_message(sender_id, response)      

                                                
                                                else:
                                                        return "ok",200
                                                        
"""                                        
        

#@app.route('/webhook', methods = ['POST'])
def log(message):
	print(message)
	sys.stdout.flush()

if __name__ == "__main__":
	app.run(debug = True, port = 8080)
