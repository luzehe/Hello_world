import imaplib
import email
from email.header import decode_header
import os
from threading import Thread
import time


host = "imap.qq.com"
username = "776133447@qq.com"
password = "cshzddapymsobcgc"

serv = imaplib.IMAP4_SSL(host, 993)
serv.login(username, password)
serv.select()

email_count = 0
num = 0
_is_first = True


def hasNew():
	global email_count
	global num
	typ, data = serv.search(None, 'ALL') 
	newlist=data[0].split()
	email_count = len(newlist)
	if email_count > num:
		num = email_count
		return data, True
	else:
		return '', False


def get_mail(data):
	newlist=data[0].split()
	typ, data = serv.fetch(newlist[-1], '(RFC822)')
	msg = email.message_from_string(data[0][1].decode('utf-8')) 
	subject_code = msg.get('Subject')
	subject, charset = decode_header(subject_code)[0]
	if charset:
		subject = subject.decode(charset)

	return subject

def comm(data):
	global _is_first
	if _is_first:
		_is_first = False
		return
	command = get_mail(data)
	if command == 'Chrome':
		print('正在执行命令:　%s' % command)
		os.system(r"start C:\Users\卢泽河\AppData\Local\Google\Chrome\Application\chrome.exe")
	if command.startswith("cmd:"):
		print('正在执行命令:　%s' % command[5:])
		os.system(command[5:])


def main():
	while True:
		try:
			data, new = hasNew()
			if new:
				comm(data)
		except Exception as e:
			print(e)
		time.sleep(1)

main()





