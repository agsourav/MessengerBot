import numpy as np
import sqlite3
class Event:
    

    def __init__(self, name,e_type,loc,zip_code,date,time,dur,max_seat,price,image_url):
        self.event_name = name
        self.event_type = e_type
        val = np.random.randint(11111,14321)
        alpha = 'prdxwer'
        self.event_id = alpha + str(5210000 + val)
        self.event_location = loc
        self.zip_code = zip_code
        #self.event_coord = coord    #{'lat': None, 'long': None}
        self.event_date = date  #{'date': None, 'month': None, 'year': 2020}
        self.event_start_time = time
        self.event_duration = dur
        self.max_seats = max_seat
        self.remaining_seats = self.max_seats
        self.price = price
        self.tax_rate = 12
        self.image_url = image_url


if __name__=="__main__":

    conn = sqlite3.connect('bookyourshow.db')
    c = conn.cursor()
    create = """CREATE TABLE events(
        ID text NOT NULL PRIMARY KEY,
        name text NOT NULL,
        type text,
        location text NOT NULL,
        zip integer
        date text,
        start_time text,
        duration integer,
        max_seats integer,
        seats_remaining integer,
        price real,
        tax_rate real,
        image_url text
        )"""

    #c.execute(create)
    insert = """INSERT INTO events(ID,name,type,location,zip,date,start_time,
    duration,max_seats,seats_remaining,price, tax_rate,image_url) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)"""

    noe = int(input())
    e = [None]*noe
    
    for i in range(noe):
        name = input("Event name:")
        e_type = input("type:")
        loc = input("place:")
        #lat = float(input("latitude:"))
        #long = float(input("longitude:"))
        zip_code = int(input("enter postal code:"))
        #day = int(input("date:"))
        #month = int(input("month:"))
        date = input("enter date of event as (dd-mm-yyyy):")
        time = input("time in 24 hrs format:")
        dur = input("duration in minutes:")
        seats = int(input("Maximum number of allocated seats:"))
        price = float(input("Enter the price per ticket(INR):"))
        image_url = input("enter image url:")
        e[i] = Event(name, e_type, loc, zip_code, date, time, dur,seats,price, image_url)
        tup = tuple([e[i].event_id, e[i].event_name, e[i].event_type,
                    e[i].event_location,e[i].zip_code, e[i].event_date,
                    e[i].event_start_time, e[i].event_duration, e[i].max_seats,
                    e[i].remaining_seats,e[i].price,e[i].tax_rate, e[i].image_url])
        c.execute(insert,tup)

    conn.commit()
    c.close()
                    
         
        
        
