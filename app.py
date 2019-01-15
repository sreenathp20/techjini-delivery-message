import threading
import time
from flask import Flask, request
from flask_api import status
import json
from process import start_runner
from lib import message

app = Flask(__name__)
msg = message.Message() #initializing message object

#recurrent service to poll scheduled message
@app.before_first_request
def activate_job():
    def run_job():
        while True:
            #print("Run recurring task")
            msg.pollMessage()
            time.sleep(10) # polling messages to deliver at on time. Can be adjusted for performance and accuracy

    thread = threading.Thread(target=run_job)
    thread.start()

# home page just show the web server is running
@app.route('/')
def hello_world():
    return 'Hello, World!'


# api for schedule a message.
# url:  http://127.0.0.1:5000/schedule-message
# method: POST
# body {"message": "text message", "delivery_time": "2019-01-15T06:15:55.765Z"} delivery time should be in iso format and should be a future time
# header: not configured, but can be configured to give authorization token
@app.route('/schedule-message', methods=['POST'])
def schedule_message():
    data = json.loads(request.data) # load request data to python dictionary
    try:
        resp = msg.schedule(data) # validate and schedule message
        if(resp["success"]): # success response for if scheduled successfully
            return json.dumps(resp), status.HTTP_202_ACCEPTED
        else: # failed to schedule after message and delivery time validation
            return json.dumps(resp), status.HTTP_400_BAD_REQUEST

    except: # failed because of exception
        resp = {"success": False, "msg": "exception"}       
        return json.dumps(resp), status.HTTP_500_INTERNAL_SERVER_ERROR



if __name__ == "__main__":
    start_runner() # start thread for polling process
    app.run() # start api web server