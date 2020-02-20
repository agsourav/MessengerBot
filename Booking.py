import numpy as np

class Booking:

    def __init__(self,username, event_id):
        alpha = 'dksork'
        val = np.random.randint(123,987)
        self.booking_id = alpha + str(56489 + val)
        self.username = username
        self.event_id = event_id

    
