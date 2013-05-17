Bitmessage Echo Server
===================

This example allows you to setup an echo server on the bitmessage network. PyBitmessage can be found here: https://github.com/Bitmessage/PyBitmessage


Setup
=====
1. Install PyBitmessage and run it once. Close PyBitmessage.
2. Place dokEchoServer.py in the same directory as BitMessage
3. Follow this guide to setup the API as following (https://bitmessage.org/wiki/API_Reference):
  * apiport = 8442
  * apiinterface = 127.0.0.1
  * apiusername = echo
  * apipassword = echoPassword
  * apinotifypath = 'Insert path to dokEchoServer.py here.'
4. Run PyBitmessage.
5. All addresses will be treated as echo addresses. The address that receives a message will be the one to return the message. (to becomes from)
