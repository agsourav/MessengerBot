import sqlite3
import pandas as pd
import numpy as np

conn = sqlite3.connect('bookyourshow.db')
c = conn.cursor()

columns_events = ['ID','name','type','location','zip','date','start_time','duration','no_of_seats']
columns_users = ['username','email']
columns_booking = ['username','event_ID']

EVENT_ID_num = np.random.randint(10000,12000)
EVENT_ID_alpha = 'daeXy'

data_events = [[EVENT_ID_alpha + str(EVENT_ID_num + 1), 'Sunburn','Music','Kolkata',700017,
        '24-02-2020','11 am',120, 200],[EVENT_ID_alpha + str(EVENT_ID_num + np.random.randint(1,50)),
                                        'CLC','Comedy','Kolkata',700027,
        '24-02-2020','8 pm',45, 40]]
#print(len(data_events), len(data_events[0]))

df = pd.DataFrame(data = data_events, columns = columns_events)
#print(df.shape)
#df.to_sql('events', conn,if_exists = 'append', index = False)

data_users = [['saag','xsfg@gmail.com']]
data_users.append(['bot', 'unknown'])
#print(data_users)
#print(len(data_users), len(data_users[0]))
df = pd.DataFrame(data = data_users, columns = columns_users)
#print(df.shape)
#df.to_sql('users', conn, if_exists = 'append', index = False)



create_table = """CREATE TABLE booking(username text NOT NULL, event_id text NOT NULL, booking_id text NOT NULL)"""

c.execute(create_table)
conn.commit()
#print(df.sample(2))
c.close()
