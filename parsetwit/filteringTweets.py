#!/bin/env/python

import tweetstream

stream = tweetstream.SampleStream("username", "password")
for tweet in stream:
	print tweet

for tweet in stream:
	print "Got tweet from %-16s\t( tweet %d, rate %.1f tweets/sec)" % ( tweet["user"]["screen_name"], stream.count, stream.rate )


