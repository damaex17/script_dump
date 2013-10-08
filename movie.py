#!/usr/bin/python
import sys
import urllib2
import json

search = sys.argv[1:]
search = "%20".join(search)
data = json.load(urllib2.urlopen('http://www.omdbapi.com/?t=%s&r=JSON&plot=full&tomatoes=true' % search))
for s in data:
	if s == "Plot":
		print '\n'+data[s]+'\n'
	elif s == "tomatoConsensus":
		print '\n'+data[s]+'\n'
	else:
		print '%20s: %s' % (s, data[s])
