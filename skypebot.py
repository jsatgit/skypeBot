#!/usr/bin/python

import Skype4Py
import time
import wikipedia
import cleverbot

# skype username of the person you want to interact with
other = "" 

# Skype4Py to interact with Skype 
skype = Skype4Py.Skype()

# Cleverbot replies
cb = cleverbot.Cleverbot()

# counts down from max to 1
def countdown(chat, max) :
	for i in reversed(range(1,int(max))) :
		chat.SendMessage("T-minus " + str(i))
		time.sleep(1)
	chat.SendMessage("Boom!")

# returns first line of wiki entry
def wiki(chat, q) :
	try :
		chat.SendMessage(wikipedia.summary(q, sentences=1)) 
	except wikipedia.WikipediaException :
		chat.SendMessage("Can't wiki that.")

# returns full wiki entry
def fullWiki(chat, q) :
	try :
		chat.SendMessage(wikipedia.summary(q)) 
	except wikipedia.WikipediaException :
		chat.SendMessage("Can't wiki that.")

def parseMsg(Message) :
	try :
		command = Message.Body.split(' ', 1)[0]
		args = Message.Body.split(' ', 1)[1]
		chat = Message.Chat
		if command == "countdown" :
			countdown(chat, args)
		elif command == "wiki" :
			wiki(chat, args)
		elif command == "wikipedia" :
			fullWiki(chat, args)
	except IndexError :
		dummy = 1

def OnMessageStatus(Message, Status) :
	if Status == 'RECEIVED' :
		if Message.FromHandle == other :
			parseMsg(Message)
			print(other + ": " + Message.Body)

			# sends reply via clever bot
			Message.Chat.SendMessage(cb.ask(Message.Body))
	elif Status == 'SENT' :
		parseMsg(Message)

def init() :
	skype.OnMessageStatus = OnMessageStatus
	skype.Attach()

def main() :
	init()
	while 1 :
		try :
			msg = raw_input()
			skype.SendMessage(other, msg)
		except(EOFError) :
			break
	
if __name__ == "__main__":
    main()
