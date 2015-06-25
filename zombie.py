import urllib.request
import urllib.parse
import codecs
import json
import random
import time
import datetime

# Do not use this as an example, this is my first ever Python script
# Tested with Python 3.4.3

# global contstants!
# (moved to config.py)
from config import *

# send message procedure
def sendSimpleMessage(chatId, text):
    try:
        data = urllib.parse.urlencode({'chat_id': format(chatId), 'text': text})
        urllib.request.urlopen(url +  'sendMessage', data.encode('utf-8'))
    except:
        return

# get the updates and reply to text messages
def doBotStuff(updateId):
    try:
        data = urllib.parse.urlencode({'offset': format(updateId), 'limit': '100', 'timeout': '60'})
        response = urllib.request.urlopen(url + 'getUpdates', data.encode('utf-8'))
        reader = codecs.getreader("utf-8")
        data = json.load(reader(response))
    except:
        return updateId

    file = open(logfilename, 'a')
    
    if (data['ok'] == True):
        for update in data['result']:
            
            # take new update id
            updateId = update['update_id'] + 1
            message = update['message']
            
            # respond if this is a message containing text
            if ('text' in message):
                file.write(format(updateId) + ': @' + message['from']['username'] + ' at ')
                file.write(datetime.datetime.fromtimestamp(int(message['date'])).strftime('%Y-%m-%d %H:%M:%S') + '\n')
                chatId = message['chat']['id']
                text = random.choice(strings)
                sendSimpleMessage(chatId, text)

    file.close()
                
    return updateId

# make sure the file exists and contains an integer
try:
    file = open(filename, 'rt')
    updateId = int(file.read())
    file.close()
except:
    with open(filename, 'w') as file:
        file.write('0')
    updateId = 0

# main program loop
while True:

    # process updates
    newUpdateId = doBotStuff(updateId)

    # write the update ID to a file and sleep 5 second if we processed updates
    if (newUpdateId != updateId):
        file = open(filename, 'wt')
        file.write(str(newUpdateId))
        file.close()
        time.sleep(5)
    else:
        # otherwise, just sleep 10 seconds
        time.sleep(10)

    # use new update ID
    updateId = newUpdateId
