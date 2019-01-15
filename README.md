# Message scheduler

This project is developd using python and flask
Github repository 
https://github.com/sreenathp20/techjini-delivery-message.git

## Setting up

Install python 2.7 and create virtulal environment
Docs: https://gist.github.com/Geoyi/d9fab4f609e9f75941946be45000632b

## Install python libraries

cd to the directory where requirements.txt is located
activate your virtualenv
run:  pip install -r requirements.txt in your shell

## Running flask app
cd to the directory where app.py
python app.py

## API document

api for schedule a message.
url:  http://127.0.0.1:5000/schedule-message
method: POST
body {"message": "text message", "delivery_time": "2019-01-15T06:15:55.765Z"} delivery time should be in iso format and should be a future time
header: not configured, but can be configured to give authorization token