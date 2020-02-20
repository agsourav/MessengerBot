from wit import Wit
import sqlite3
import numpy as np
access_token = "ILVTMHD3NLKQY2XH7FAB5U2WG6MHAXXA"
rand = 4432
client = Wit(access_token = access_token)

conn = sqlite3.connect('bookyourshow.db', check_same_thread = False)
c = conn.cursor()
#message_text = "I want to query events"
#resp = client.message(message_text)
#print(resp['entities'])
def wit_handleMessage(sender_id, message_event):
    categories = {'querytype':None, 'eventtype':None, 'greet':None,'ok':None}
    
    if 'text' in message_event:
        response = 'Hello people'
        response_txt = "You sent the message: "+ message_event['text']
        #return {'text':response_txt}
        try:
            res = client.message(message_event['text'])
            #return {'text':str(res)}
            entities = list(res['entities'])
            for entity in entities:
                categories[entity] = res['entities'][entity][0]['value']

            for category,value in categories.items():
                if value:
                    if category == 'ok':
                        response = {'text':'ok'}
                        return response
                    elif category == 'greet':
                        response = greetings(value)
                        return response
                    elif category == 'querytype':
                        if value == 'events':
                            events = view_event()
                            elements = []
                            for event in events:
                                #(ID,name,type,location,zip,date,start_time,duration,max_seats, seats_remaining,price,tax_rate,image_url)
                                sub = str(event[3])+':'+str(event[4])+'\n'+event[5]+':'+event[6]+' hours(IST)'+'\nPrice(INR):'+str(event[10])+'\nClick below for more information'
                                element = {
                                    'title':event[1]+' :: '+event[2],
                                    'image_url':event[12],
                                    'subtitle': sub,
                                    'buttons':[
                                        {
                                            'type':'postback',
                                            'title':'more info',
                                            'payload':event[1]
                                            },
                                        {
                                            'type':'postback',
                                            'title':'book ticket',
                                            'payload':str(event[1]+'-book')
                                            }]
                                    }
                                elements.append(element)
                            response = {
                                "attachment":{
                                    "type":"template",
                                    "payload": {
                                        "template_type":"generic",
                                        "elements":elements
                                        }
                                    }
                                }
        
                        elif value == 'bookings':
                            res = view_bookings(sender_id)
                            response = res
                            #response = {'text':'view here!'}
                        return response
                    
                        #response = 'You may book tickets or view events or view bookings'
                    elif category == 'eventtype':
                        events = view_events_by_query('type',value)    #querying events
                        #(ID, name, type, location, zip, date, start_time, duration, max_seats, seats_remaining, price, tax_rate, image_url)
                        elements = [{
                                    'title':event[1]+' :: '+event[2],
                                    'image_url':event[12],
                                    'subtitle': sub,
                                    'buttons':[
                                        {
                                            'type':'postback',
                                            'title':'more info',
                                            'payload':event[1]
                                            },
                                        {
                                            'type':'postback',
                                            'title':'book ticket',
                                            'payload':str(event[1]+'-book')
                                            }]
                                    }]
                        response = {
                                "attachment":{
                                    "type":"template",
                                    "payload": {
                                        "template_type":"generic",
                                        "elements":elements
                                        }
                                    }
                                }
                        
                else:
                    response = greetings('hi')
                return response
        except:
            response = greetings('hi')
            
                
    elif 'attachments' in message_event:
        attachment_url = None
        response = {
            "text":"you sent an attachment"
            }
        #print('\n',attachment_url)
        try:
            attachment_url = message_event['attachments'][0]['payload']['url']
        except:
            print('attachment_error')
        if attachment_url:
            elements = [{
                "title":"Is this your picture?",
                "subtitle":"Tap a button to answer",
                "image_url": attachment_url,
                "buttons":[
                    {
                        "type":"postback",
                        "title":"Yes!",
                        "payload":"yes",
                        },
                    {
                        "type":"postback",
                        "title":"No!",
                        "payload":"no",
                        }
                    ]}]
            response = elements
        return response
    #return wit_sendMessage(sender_id, response)
    #response = client.message(message_text)
    else:
        response = greetings('hi')
        return response
    


def wit_postback(sender_id, postback):
    #handling postback requests here
    payload = postback['payload']
    response = postback['payload']
    #return {'text':str(response)}
    select = """SELECT name from events"""
    event_names = c.execute(select).fetchall()
    if(payload == 'exit'):
        response = {
            'text':'bye bye...'
            }
    elif(payload == 'yes'):
        response = {
            "text": "Thanks!"
            }
    elif(payload == 'no'):
        response = {
            "text": "Oops, keep going!"
            }
    elif (payload,) in event_names:
        event = view_events_by_query('name',payload)[0]
        info = event[1]+'\n'+event[2]+' show'+'\nStarts at '+event[6]+' for duration '+ str(event[7]) + ' minutes' + '\nPrice(exclusive of taxes):'+str(event[10])+'\nnumber of seats remaining:'+str(event[9])
        
        res = greetings('hi')
        res['text'] = info + '\n' + res['text']
        
        return res
    elif payload.endswith('book'):
        res, status = book_event_ticket(sender_id,payload)
        #return {'text': str(status)}
        if status == 5:
            return res
        elif status == 102:
            event_name = payload.split('-')[0]
            booking = view_bookings(sender_id)
            txt = str(booking)
            return {'text':'checking booking'}
        elif status == 0:
            return {'text': 'desired ticket is unavailable'}
        else:
            return {'text':'checking payload'}
    elif payload.endswith('confirm'):
        event_name = payload.split('-')[0]
        res,status = confirm_booking(sender_id,event_name)
        if status == 200:
            response = res
        else:
            response = res

    else:
        response = {'text':str(payload)}
        return response
        #event = view_events_by_query('ID',payload)[0]
        
                    
    
    return response

def wit_sendMessage(sender_id, response):
    request_body = {
        "recipient": {
            "id": sender_id
            },
        "message": response
        }
    return request_body

def validate_booking(user,event):
    #validate and confirm
    if event[-1]:
        booking_id = user + event[1][:2] + str(rand)
        v = validate_bookingID(booking_id)
            #return v
        return v
    else:
        return 0

def validate_bookingID(id_):
    select = """SELECT booking_id from booking where booking_id = ?"""
    e = c.execute(select,(id_,)).fetchall()
    #return e
    if len(e)==0:
        return 5
    else:
        return 102
def book_event_ticket(user, payload):
    event = payload.split('-')[0]
    events = view_events_by_query('name',event)
    if(len(events)>0):
        v = validate_booking(user,events[0])
        if v == 5:
            txt = event
            response = {
                "attachment":{
                  "type":"template",
                  "payload":{
                    "template_type":"button",
                    "text":txt,
                    "buttons":[
                      {
                        "type":"postback",
                        "title":"Confirm booking",
                        "payload":event+'-'+'confirm'
                      }
                    ]
                  }
                }
              }
            return response,v
        else:
            return {'text':'failed'},v
        
def confirm_booking(user, event):
    insert = """INSERT INTO booking(username,event,booking_id,payment_method,price) VALUES(?,?,?,?,?)"""
    booking_id = user + event[:2] + str(rand)
    v = validate_bookingID(booking_id)
    select = """SELECT booking.booking_id, booking.username, e.name, e.location,e.date,e.price, e.tax_rate, e.type,e.image_url
FROM booking, events as e WHERE booking.event = e.name AND booking.booking_id = ?"""
    status = 102
    if v == 5:
        sql = """SELECT events.price, events.tax_rate, events.seats_remaining FROM events WHERE events.name = ?"""
        e = c.execute(sql,(event,)).fetchall()
        total = e[0][0]*e[0][1]/100.0
        value = [str(user), event, booking_id,"visa",str(total)]
        c.execute(insert,value)
        update = """UPDATE events SET seats_remaining = ? WHERE name = ?"""
        c.execute(update,(e[0][2]-1,event))
        conn.commit()
        status = 200
    else:
        status = v

    event = c.execute(select,(booking_id,)).fetchall()[0]
    r = {
    "attachment":{
      "type":"template",
      "payload":{
        "template_type":"receipt",
        "recipient_name":str(user),
        "order_number":booking_id,
        "currency":"INR",
        "payment_method":"Visa",        
        "order_url":"http://petersapparel.parseapp.com/order?order_id=123456",
        "timestamp":"1428444852",         
        "address":{
          "street_1":"Online",
          "street_2":"",
          "city":"Kolkata",
          "postal_code":"457",
          "state":"WB",
          "country":"INDIA"
        },
        "summary":{
          "subtotal":str(event[5]),
          "shipping_cost":None,
          "total_tax":str(event[5]*event[6]/100),
          "total_cost":str(event[5]+event[5]*event[6]/100)
        },
        "adjustments":[
        ],
        "elements":[
          {
            "title":event[2],
            "subtitle":event[7],
            "quantity":1,
            "price":event[5],
            "currency":"INR",
            "image_url":event[8]
          }
        ]
      }
    }
  }
    return r,status
    

def view_bookings(sender_id):
    #return {'text':'you may view your bookings here...'}    
    select_query = select_query = """SELECT booking.username, e.name, e.type, e.date, e.location, e.start_time,
e.duration, booking_id, booking.price, payment_method, e.image_url from events as e, booking WHERE booking.event = e.name AND booking.username = ?"""
    val = (sender_id,)
    booking = c.execute(select_query,val).fetchall()
    elements = []
    for b in booking:
        title = str(b[1]+'::'+b[2])
        element = {
            "title":title,
            "image_url":b[10],
            "subtitle":str('booking id: '+b[7]),
            "default_action": {
              "type": "web_url",
              "url": "https://petersfancybrownhats.com/view?item=103",
              "webview_height_ratio": "compact",
            },
            "buttons":[
              {
                "type":"web_url",
                "url":"https://petersfancybrownhats.com",
                "title":"View Website"
              },{
                "type":"postback",
                "title":"Start Chatting",
                "payload":"DEVELOPER_DEFINED_PAYLOAD"
              }
              ]
            }
        elements.append(element)
            
    #return {'text':str(elements)}
    #retrun str(elements)
    #return {'text':'finished search...'}
    response = {
    "attachment":{
      "type":"template",
      "payload":{
        "template_type":"generic",
        "elements":elements[:2]
             
          }
      }
  }
    return response

    
        
def view_bookings_by_event(sender_id,name):
    return {'text':'view your bookings here'}
    select_query = """SELECT e.name, e.type, e.date, e.location, e.start_time,
    e.duration, booking_id, price, payment_method, tax from events as e, booking
    WHERE booking.event = ? AND booking.event = e.name AND username = ?"""
    val = (name,sender_id)
    book = c.execute(select_query,val).fetchall()
    return book
    elements = []
    for event in book:
        element = {
            'title': event[1],
            'image_url': "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fupload.wikimedia.org%2Fwikipedia%2Fen%2Fthumb%2F4%2F47%2FRazerComms_icon.svg%2F768px-RazerComms_icon.svg.png&f=1&nofb=1"
            }
        elements.append(element)
    return elements

def create_element(events):
    elements = []
    for event in events:
        element = {
         'title': event[1],
         'subtitle': event[5],
         'buttons': [{
         'type':'postback',
         'title':'read more',
         'payload': event[0]
                    }],
         'image_url': "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fi.ytimg.com%2Fvi%2FOnaFxH-Bec0%2Fmaxresdefault.jpg&f=1&nofb=1"
                
           }
        elements.append(element)
    return elements
       
def view_event():
    select_query = """SELECT * from events"""
    events = c.execute(select_query).fetchall() 
    return events

def view_events_by_query(col, t):
    select_query = "SELECT * from events WHERE {} = ?".format(col)
    events = c.execute(select_query,(t,)).fetchall()
    return events


def get_started():
    elements = [{
        'messaging_type': 'RESPONSE',
        'message': {
            'text': 'How may I help you?',
            'quick_replies':[
                {
                    'content_type':'text',
                    'title':'view events',
                    'payload':'events'
                },
                {
                    'content_type':'text',
                    'title':'view your bookings',
                    'payload':'bookings'
                },
                {
                    'content_type':'text',
                    'title':'bye',
                    'payload':'exit'
                    }]
            }
        }]
    return elements


def greetings(greeting_text):
    wish = ["good morning", "good evening","good afternoon"]
    response = "How may I help you?"
    if greeting_text in wish:
        response = greeting_text + '.' + response
    res1 = {
        'text':response,
        }
    #sending only message responses
    res = {
            'text': response,
            'quick_replies': [{
                'content_type':'text',
                'title':'query events',
                'payload':'query events',
                'image_url':'http://www.inma.org/modules/event/2015EditorialIdeasDay/images/icons/icon_innovation_chiefs.png'
                },
                             {
                
                'content_type':'text',
                'title':'query bookings',
                'payload':'query bookings',
                'image_url':'http://brassnecktheatre.com/wp-content/uploads/2014/01/merchandise-icon.png'
                },
                             {
                'content_type':'text',
                'title':'exit',
                'payload':'exit',
                'image_url':'http://brassnecktheatre.com/wp-content/uploads/2014/01/merchandise-icon.png'
                }
                             ]}
     
        
    return res

#print(len(view_bookings('bot')))
#print(book_event_ticket('bot','djsjpse2930820'))
#print(view_events_by_query('type', 'music'))
#wit_response("Where is comedy show?")
#wit_response("hi")
#for event in cat:
#    print(cat[event])
