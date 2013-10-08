#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

mapping = zip(
	(1000,900,500,400,100,90,50,40,10,9,5,4,1),
	("M","CM","D","CD","C","XC","L","XL","X","IX","V","IV","I"))

def int2rom(num):
	value = []
	for integer, roman in mapping:
		counter = int(num/integer)
		value.append(roman*counter)
		num -= integer*counter
	return "".join(value)

def rom2int(num):
	num = num.upper()
	cursor = value = 0
	for integer, roman in mapping:
		while num[cursor:cursor + len(roman)] == roman:
			value += integer
			cursor += len(roman)
	return value
	
while True:
	user = sys.stdin.readline()
	if not user:
		break
	try: 
		print(int2rom(int(user)))
	except ValueError:
		print rom2int(user.rsplit('\n')[0])
