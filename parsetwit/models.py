from django.db import models
import urllib
import urllib2
import socket
import time
import anyjson
import tweetstream
import Queue
import threading
import cPickle
import os
import sys
from datetime import datetime

# Create your models here.
class Matches(models.Model):
	perfectmatches = models.CharField(max_length=200)
	pub_date = models.DateTimeField('date published')
	def __unicode__(self):
		return 'perfectmatches' + ' matched at ' + 'pub_date'


class Word(models.Model):
	word = models.CharField(max_length=200)
	def __unicode__(self):
		return 'word'

#this class is so that a new User can be instantiated whenever the 400 retrieves limit is reached
class User(models.Model):
	name = models.CharField(max_length=20)
	password = models.CharField(max_length=15)
	def __unicode__(self):
		return name

class TweetStream(models.Model):

    def __init__(self, username, password, url="spritzer"):
        self._conn = None
        self._rate_ts = None
        self._rate_cnt = 0
        self._username = username
        self._password = password

        self.rate_period = 10 # in seconds
        self.connected = False
        self.starttime = None
        self.count = 0
        self.rate = 0
        self.user_agent = USER_AGENT
        self.url = URLS.get(url, url)

    def __iter__(self):
        return self

    def __enter__(self):
        return self

    def __exit__(self, *params):
        self.close()
        return False

    def _init_conn(self):
        """Open the connection to the twitter server"""
        headers = {'User-Agent': self.user_agent}
        req = urllib2.Request(self.url, self._get_post_data(), headers)

        password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
        password_mgr.add_password(None, self.url, self._username,
                                  self._password)
        handler = urllib2.HTTPBasicAuthHandler(password_mgr)
        opener = urllib2.build_opener(handler)

        try:
            self._conn = opener.open(req)
        except urllib2.HTTPError, exception:
            if exception.code == 401:
                raise AuthenticationError("Access denied")
            else: # re raise. No idea what would cause this, so want to know
                raise
        except urllib2.URLError, exception:
            raise ConnectionError(exception.reason)

        self.connected = True
        if not self.starttime:
            self.starttime = time.time()
        if not self._rate_ts:
            self._rate_ts = time.time()

    def _get_post_data(self):
        """Subclasses that need to add post data to the request can override
        this method and return post data. The data should be in the format
        returned by urllib.urlencode."""
        return None

    def next(self):
        """Return the next available tweet. This call is blocking!"""
        while True:
            try:
                if not self.connected:
                    self._init_conn()

                rate_time = time.time() - self._rate_ts
                if not self._rate_ts or rate_time > self.rate_period:
                    self.rate = self._rate_cnt / rate_time
                    self._rate_cnt = 0
                    self._rate_ts = time.time()

                data = self._conn.readline()
                if data == "": # something is wrong
                    self.close()
                    raise ConnectionError("Got entry of length 0. Disconnected")
                elif data.isspace():
                    continue

                data = anyjson.deserialize(data)
                self.count += 1
                self._rate_cnt += 1
                return data

            except ValueError, e:
                self.close()
                raise ConnectionError("Got invalid data from twitter", details=data)

            except socket.error, e:
                self.close()
                raise ConnectionError("Server disconnected")


    def close(self):
        """
        Close the connection to the streaming server.
        """
        self.connected = False
        if self._conn:
            self._conn.close()

	
class StreamCollector(models.Model):
    """ List of keywords to track"""
    trackingK = [':)']
    
    """ Limit (how many tweets should be received before quitting ) """
    limit = 1000000
    
    """ Twitter user/pass"""
    twitterUser = 'your_twitter_username'
    twitterPass = 'your_twitter_pass'
    
    def __init__(self,tweetsQ,stop_event):
        threading.Thread.__init__(self)
        self.q = tweetsQ
        self.stop_event = stop_event
        self.start_t = time.time()
        self.c = 0
        
    def collect(self):
        stream = tweetstream.TrackStream(self.twitterUser, self.twitterPass ,keywords=self.trackingK, url='https://stream.twitter.com/1/statuses/filter.json')  
        for tweet in stream:
            
            if self.c and self.c % 1000 == 0:
                print "done with %d tweets in %s" % (self.c,datetime.now())
                
                
            if self.c >= self.limit:
                raise Exception('done');
            
            try:
                self.q.put(tweet)
            except Exception, e:
                print e
            
            self.c += 1
     
    def run(self):
        while True:
            try:
                self.collect()
            except Exception, e:
                print e
                if self.c >= self.limit:
                    self.stop_event.set()
                    break

class WordFinder(models.Model):
	statsData = {}
	dataDir = "/DjangoAppData/apps/parsetwit/data"
	limit = {}
	skip = 0
	p2_f_limit = 0.75

	def __init__(self, training_data_file='namesOfTeams.dat', comparison_file='matching_tweets.dat'):
		
		self.list1 = FrequencyDetectTrainData(data_file = training_data_file)
		self.list2 = ParameterTrainData(data_file = comparison_file)

		self.sportsClassifier = SportsDetect(supportedSports)

		self.training_data_file_p1 = FrequencyDetectTrainer()
		self.comparison_file_p1 = ParameterDataTrainer()


class FrequencyDetectTrainer():

	tk = WordGramTokenizer()

	def addRow(self,text,label,event):
		print "...."


class EventDetect():

	def detect(self, tex):
		#Detect the kind of event: NFL, MLB, Superbowl, Rose Bowl, etc

		if not isinstance(text, unicode):
			raise Exception('not unicode')

		trigrams = self.tk.tokenize(text)

		score = duct([(event, 0) for event in self.event_trigrams.keys()])
		total = sum(trigrams.values())

		for trigram, count in trigrams.items():
			for event, frequencies in self.event_trigrams.items():
				#normalizing
				scores[lang] += (float(frequencies[trigram]) / float(frequencies.N())) * (float(count) / float(total))
			
		best_match = sorted(scores.items(), key=lambda x: x[1], reverse=True)[0]

		if best_match[1] == 0:
			return ('other', 0)
		else:
			return best_match


		

	


	
