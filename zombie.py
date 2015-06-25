import urllib.request
import urllib.parse
import codecs
import json
import random
import datetime
import time

# Do not use this as an example, this is my first ever Python script
# Tested with Python 3.4.3

# global contstants!
# token from config.py
from config import token
strings = ['Aaarghhh!!!', 'Braaiiinnzzz..', 'Grmbblrr..', 'GRRRRRR...!!', 'Bluuughhrr..']
url = 'https://api.telegram.org/bot' + token + '/'
filename = 'offset.txt'  # updateID offset to prevent multiple responses
logfilename = 'log.txt'  # logfile


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
    
    if data['ok'] == True:
        for update in data['result']:
            
            # take new update id
            updateId = update['update_id'] + 1
            message = update['message']
            
            # respond if this is a message containing text
            if 'text' in message:
                messagetext = str(message['text'])

                # skip any commands except "/start" because we don't do commands in zombieland
                if messagetext.startswith('/') and not messagetext.startswith('/start'):
                    continue

                # write a little in the log file
                file.write(format(updateId) + ': user ' + format(message['from']['id']))
                if ('username' in message['from']):
                    file.write(' (@' + message['from']['username'] + ')')
                file.write(' at ' + datetime.datetime.fromtimestamp(int(message['date'])).strftime('%Y-%m-%d %H:%M:%S') + '\n')

                # compose and send a reply (in zombie language)
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

    # write the update ID to a file and sleep 3 seconds if we processed updates
    if (newUpdateId != updateId):
        file = open(filename, 'wt')
        file.write(str(newUpdateId))
        file.close()
        time.sleep(3)
    else:
        # otherwise, sleep 1 second; we can wait some more during long polling if we have to.
        time.sleep(1)

    # use new update ID
    updateId = newUpdateId
