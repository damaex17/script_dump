#!/usr/bin/python

import sys
import os
import whisper
import time
import math
import smtplib
import sp_lib
import urllib2, base64
from types import *
from email.MIMEText import MIMEText

path = sys.argv[1]
now = int(time.time())
from_ = now - 10800 # six hours
informWho = ''
base64string = base64.encodestring('%s:%s' % ('', '')).rstrip('\n')



def send_mail(body, receiver):
	s = smtplib.SMTP('localhost')
	s.sendmail("graphiteSpike@%s" % (sp_lib.hostname()), receiver, body)
	s.quit()


def std_dev(list, avg):
	n, c = 0, 0
	for item in list:
		n += math.pow((item-avg), 2)
		c += 1
	if c != 0:
		return math.sqrt(n/c)
	else: 
		return 'unknown'

	
def find_whisper(path):
	WhisperFiles = []
	for path, dir, files in os.walk(path):	
		for file in files:
			WhisperFiles.append('%s/%s' % (path, file))
	return WhisperFiles


def clean_list_from_none(list):
	ReturnList = []
	for data in list:
		if type(data) is not NoneType:
			ReturnList.append(float(data))
	if len(ReturnList) != 0:
		return ReturnList
	else:
		return []


def calc_avg(list):
	c = 0
	avg_sum = 0
	for data in list:
		if type(data) is not NoneType:
			avg_sum += data
			c += 1
	if c != 0:
		return (avg_sum/c)
	else:
		return 'unknown'


def build_url(filename):
	ret = ''	
	list = filename.replace('/', ' ').split()[4:]
	for item in list:
		ret += (item + '.')
	return ret[:-5]


def get_url_data(path, auth):
	url = 'https://graphite.domain.com/render?from=-300minutes&until=now&target=%s&rawData' % path
	request = urllib2.Request(url)
	request.add_header('Authorization', 'Basic %s' % auth)
	return urllib2.urlopen(request).read()


def change_value_type(list):
	newList = []
	for item in list:
		try:
			item = float(item)
			newList.append(item)
		except:
			continue
	return newList


def main():
	WhisperFiles = find_whisper(path)
	for WhisperFile in WhisperFiles:
		(timeInfo, values) =  get_url_data(build_url(WhisperFile), base64string).split('|')
		timeInfo = change_value_type(timeInfo.split(',')[1:])
		values = change_value_type(values.split(','))
		score = 0
		# uncomment the following to ignore values in the cache and only use values on the disk
		#(timeInfo, values) = whisper.fetch(WhisperFile, from_, now)
		cl = clean_list_from_none(values)
		ll = len(cl)
		# create 100%, 25% and 10% sized time window
		cl25, cl10 = cl[-(ll/4):], cl[-(ll/10):]
		avg, avg25, avg10 = calc_avg(cl), calc_avg(cl25), calc_avg(cl10)
		if avg == 'unknown': continue
		if len(cl) < 1 or cl[-1] <= 2: continue
		# get stdev from 100%, 25% and 10% lists
		sd, sd25, sd10 = std_dev(cl, avg), std_dev(cl25, avg25), std_dev(cl10, avg10)
		# this should be more advanced right here; multiple timeranges
		if cl[-1] > (avg + (4*sd)) and len(cl) > 1:
			score += 2 
		if cl[-1] > (avg25 + (4*sd25)) and len(cl) > 1:
			score += 2 
		if cl[-1] > (avg10 + (4*sd10)) and len(cl) > 1:
			score += 2 
		if score >= 4 and cl[-1] >= 5:
			message = '#'*25 + '\n'
			message += time.asctime(time.localtime(timeInfo[1])) + '\n'
			message += '#'*25 + '\n'
			message += 'Score    : %s\n' % (score)
			message += 'file     : %s\n' % (WhisperFile)
			message += 'avg      : %s\n' % (avg)
			message += 'avg25    : %s\n' % (avg25)
			message += 'avg10    : %s\n\n' % (avg10)
			message += 'sd       : %s\n' % (sd)
			message += 'sd25     : %s\n' % (sd25)
			message += 'sd10     : %s\n\n' % (sd10)
			message += 'val      : %s\n' % cl[-1]
			message += 'alarm    : %s\n' %(avg + (4*sd))
			message += 'alarm25  : %s\n' %(avg25 + (4*sd25))
			message += 'alarm10  : %s\n\n' %(avg10 + (4*sd10))
			message += 'no. val  : %s\n' % len(cl)
			message += 'val exmp : %s\n\n' % (cl[-10:])
			message += 'https://graphite.domain.com/render?from=-360minutes&until=now&height=400&width=800&target=%s' % (build_url(WhisperFile))
			message += '\n'
			msg = MIMEText(message)
			msg['Subject'] = 'graphiteSpike on %s %s %s' % (WhisperFile.split('/')[-3], WhisperFile.split('/')[-2], WhisperFile.split('/')[-1])
			send_mail(msg.as_string(), informWho)
			print message


if __name__ == "__main__":
	main()
