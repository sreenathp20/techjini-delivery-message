from datetime import datetime
import pytz
import dateutil.parser
import time

utc=pytz.UTC



class Message():
    def __init__(self):
        self.data = [] # initializing empty message list

    # validate message before scheduling it
    def validate(self, data):
        err = []
        if(not data["message"]):
            err.append("Message not available")
        if(not data["delivery_time"]):
            err.append("Delivery time not available")
        else:
            diff = self.isValidTime(data["delivery_time"])
            if(diff <= 0):
                err.append("Delivery time is already over")
        return err

    # validate delivery time for future time
    def isValidTime(self, t):
        a = datetime.now(pytz.UTC)
        delivery_time = dateutil.parser.parse(t)
        #print a, " a ", delivery_time, " delivery_time"
        c = delivery_time - a
        daysDiff = c.days
        mins = divmod(c.days * 86400 + c.seconds, 60)[0]
        #print daysDiff, "daysDiff", mins, " mins"
        return mins

    # schedule message
    def schedule(self, data):
        err = self.validate(data)
        res = {}
        if(len(err) > 0):
            res["success"] = False
            res["msg"] = err
        else:
            self.data.append(data)
            res["success"] = True
            res["msg"] = "Accepted"
            #print self.data, " self.data"
        return res

    # poll message for delivery at on time
    def pollMessage(self):
        if(self.data):
            i = 0
            for d in self.data:
                #print(d["message"], d["delivery_time"])
                diff = self.isValidTime(d["delivery_time"])
                #print diff, d["delivery_time"]
                if(diff <= 0):
                    print d["message"]
                    self.data = self.data[:i]+self.data[i+1:]
                i += 1
        else:
            print("No messages scheduled")