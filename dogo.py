#!/usr/bin/env python

from email.message import EmailMessage

import requests
import smtplib
import imghdr
import json
import sys

# open config file
config = open('config', 'r')
lines = config.readlines()

api = ""
field = ""
subject = ""
sender = ""
recipients = []
content = ""
password = ""

# parse config file
for line in lines:

    line = line.strip('\n')
    key, value = line.split(':', 1)

    if key == "api":
        api = value
    elif key == "field":
        field = value
    elif key == "subject":
        subject = value
    elif key == "from":
        sender = value
    elif key == "to":
        recipients.append(value)
    elif key == "content":
        content = value
    elif key == "auth":
        password = value

# fetch content
response = requests.get(api)
picture_url = response.json()[field]
picture = requests.get(picture_url)

# assemble message
msg = EmailMessage()

msg["Subject"] = subject
msg["From"] = sender
msg["To"] = recipients

msg.set_content(content)

# write the picture to file
with open('image.jpg', 'wb') as file:
    file.write(picture.content)
    file.close()

# read the picture data
with open('image.jpg', 'rb') as file:
    image_data = file.read()
    image_type = imghdr.what(file.name)
    image_name = file.name

# add attachment
msg.add_attachment(image_data,
                   maintype='image',
                   subtype=image_type,
                   filename=image_name)

# send message
with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(sender, password)
    smtp.send_message(msg)

sys.exit()

