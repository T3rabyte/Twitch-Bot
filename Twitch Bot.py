import socket
import pyautogui
import threading

SERVER = "irc.twitch.tv"
PORT = 6667
PASS = ""
BOT	= "TwitchBot"
CHANNEL = "frosthazard"

message = ""

irc = socket.socket()

irc.connect((SERVER, PORT))
irc.send(("PASS " + PASS + "\n" +
	     "NICK " + BOT + "\n" + 
	     "JOIN #" + CHANNEL + "\n").encode())

def gamecontrol():
	global message
	while True:
		if message != "":
			if "omhoog" == message.lower():
				pyautogui.keyDown('up')
				message = ""
				pyautogui.keyUp('up')

			elif "beneden" == message.lower():
				pyautogui.keyDown('down')
				message = ""
				pyautogui.keyUp('down')

			elif "links" == message.lower():
				pyautogui.keyDown('left')
				message = ""
				pyautogui.keyUp('left')

			elif "rechts" == message.lower():
				pyautogui.keyDown('right')
				message = ""
				pyautogui.keyUp('right')

			elif "aknop" == message.lower():
				pyautogui.keyDown('s')
				message = ""
				pyautogui.keyUp('s')

			elif "bknop" == message.lower():
				pyautogui.keyDown('a')
				message = ""
				pyautogui.keyUp('a')

			elif "start" == message.lower():
				pyautogui.keyDown('enter')
				message = ""
				pyautogui.keyUp('enter')

			else:
				message = ""
				pass
		else:
			pass

def twitch():
	def joinchat():
		Loading = True
		while Loading:

			readbufferJoin = irc.recv(1024)
			readbufferJoin = readbufferJoin.decode()

			for line in readbufferJoin.split("\n")[0:-1]:
				print(line)
				Loading = loadingComplete(line)

	def loadingComplete(line):
		if ("End of /NAMES list" in line):
			print("Bot has joined " + CHANNEL + "'s Channel!")
			seandMessage(irc, "Bot joined the chat room")
			return False
		else:
			return True

	def seandMessage(irc, message):
		messageTemp = "PRIVMSG #" + CHANNEL + " :" + message
		irc.send((messageTemp + "\n").encode())

	def getUser(line):
		separate = line.split(":", 2)
		user = separate[1].split("!", 1)[0]
		return user

	def getMessage(line):
		global message
		try:
			message = (line.split(":",2))[2]
		except:
			message = ""
		return message

	def Console(line):
		if "PRIVMSG" in line:
			return False
		else:
			return True

	joinchat()

	while  True:
		try:
			readbuffer = irc.recv(1024).decode()
		except:
			readbuffer = ""
		for line in readbuffer.split("\r\n"):
			if line == "":
				continue
			elif "PING" in line and Console(line):
				msgg = "PONG tmi.twitch.tv\r\n".encode()
				irc.send(msgg)
				print(msgg)
				continue
			else:
				user = getUser(line)
				message = getMessage(line)
				print(user + ": " + message)

if __name__ == '__main__':
	t1 = threading.Thread(target = twitch)
	t1.start()
	t2 = threading.Thread(target = gamecontrol)
	t2.start()