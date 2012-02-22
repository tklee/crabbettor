from django.db import models

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
