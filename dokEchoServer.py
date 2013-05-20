#!/usr/bin/env python2.7
# Created by Adam Melton (.dok) referenceing https://bitmessage.org/wiki/API_Reference for API documentation
# Distributed under the MIT/X11 software license. See the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

# This is an example of an echo server for PyBitmessage 0.3.0, by .dok (Version 0.2.1)

import ConfigParser
import xmlrpclib
import getopt
import json
import sys
import time
from time import strftime, gmtime

versionNo = 2.1

def logEcho(recTime,bmAddress):
    global versionNo
    config = ConfigParser.RawConfigParser()
    echoLogFile = 'EchoLog.dat'
    config.read(echoLogFile)

    try: #try to open the file
        config.get('EchoServer','processedTotal')
    except:# if it fails, then initialize the EchoLog.dat file since this is the first time running the program
        print 'Initializing EchoLog.dat'
        config.add_section('EchoServer')
        config.add_section('EchoLogs')
        
        config.set('EchoServer','versionNumber',str(versionNo))
        config.set('EchoServer','processedTotal','0')

    processedTotal = int(config.get('EchoServer','processedTotal'))
    processedTotal = processedTotal + 1
    
    config.set('EchoServer','processedTotal',str(processedTotal)) #echo count
    config.set('EchoLogs',recTime,bmAddress) #message information
    
    with open(echoLogFile, 'wb') as configfile: #updates the total number of processed messages
        config.write(configfile)

    print 'Echo successfully logged.'


def processEcho():
    api = xmlrpclib.ServerProxy("http://echo:echoPassword@localhost:8442/") #Connect to BitMessage using these api credentials

    print 'Loaded from API successfully.'
    timeStamp = gmtime() #set the timestamp before processing (to get the most accurate time)

    inboxMessages = json.loads(api.getAllInboxMessages()) #Parse json data in to python data structure
    print 'Loaded all inbox messages for processing.'
    
    newestMessage = (len(inboxMessages['inboxMessages']) - 1) #Find the newest message (the only to echo)
    replyAddress = inboxMessages['inboxMessages'][newestMessage]['fromAddress'] #Get the return address
    myAddress = inboxMessages['inboxMessages'][newestMessage]['toAddress'] #Get my address
    subject = 'ECHO'.encode('base64') #Set the subject

    print 'Loaded and parsed data. Ready to build outgoing message.'
    
    message = inboxMessages['inboxMessages'][newestMessage]['message'].decode('base64') #Gets the message sent by the user
    if (len(message) > 256):
        message = (message[:256] + '... Truncated to 256 characters.\n')
        
    echoFooter = "INSERT YOUR TEXT HERE" #This is where what you would like the footer to say. Be sure to add the line breaks
    
    echoMessage = ('Message successfully received at ' + strftime("%Y-%m-%d %H:%M:%S",timeStamp) + ' UTC/GMT.\n' + 
    '-------------------------------------------------------------------------------\n' + message + '\n\n\n'+ echoFooter)
    
    echoMessage = echoMessage.encode('base64') #Encode the message.

    print 'Message built, ready to send. Sending...'
    api.sendMessage(replyAddress,myAddress,subject,echoMessage) #build the message and send it
    print 'Sent.'

    print 'Begin logging echo.'
    logEcho(strftime("%Y_%m_%d-%H_%M_%S",timeStamp), replyAddress) #Logs the echo to the EchoLog.dat file 

    if (newestMessage > 25): #Delete oldest message, trying to keep only 25 messages in the inbox. Only deletes one so it won't clear out your inbox (you can do that).
        msgId = inboxMessages['inboxMessages'][0]['msgid'] #gets the message ID of the oldest message in the inbox (index 0)
        api.trashMessage(msgId)
        print 'Oldest message deleted.'


def main():
    arg = sys.argv[1]
        
    if arg == "startingUp":
        sys.exit()
    elif arg == "newMessage":
        processEcho() #carries out the echo
        print 'Done.'
        sys.exit() #Done, exit
        
    elif arg == "newBroadcast":
        sys.exit()
    else:
        assert False, "unhandled option"
        sys.exit() #Not a relevant argument, exit
        
if __name__ =="__main__":
    main()
