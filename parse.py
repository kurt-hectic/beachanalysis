from datetime import datetime 
import re
import sqlite3
import sys

with sqlite3.connect('messages.db') as conn:

	c=conn.cursor()
	with open('messages.txt', encoding='utf-8') as file:
		content = file.readlines()
		i=0
		while i<len(content):
			message = content[i]
			j=0
			
			while (i+j+1)<len(content) and not re.match('\d{2}/\d{2}/\d{4}, \d{2}:\d{2} - ',content[i+j+1]):
				messagecont = content[i+j+1]
				#print("adding multiline {}".format(messagecont))
				message = "{} {}".format(message,messagecont)
				i=i+1
				
			i=i+j
			
			p = message.find(' - ')
			date = message[0:p-1].strip()
			message = message[p+2:].strip()
				
			
			dt = datetime.strptime(date,'%d/%m/%Y, %H:%M')
			p = message.find(':')
			if (p==-1):
				system = True
				author = "system"
				message = message
			else: 
				system = False
				author = message[0:p].strip()
				message = message[p+1:].strip()
			
			#print("On {} {} wrote {}".format(dt,author,message))
			params = [dt,author,message,system]
			c.execute("INSERT INTO messages (postdate,author,message,system) VALUES (?,?,?,?)",params)
			
			
			i=i+1
			
	conn.commit()
	