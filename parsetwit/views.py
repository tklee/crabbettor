# Create your views here.
from django.template import Context, loader
from django.http import HttpResponse

def index(request):
	t = loader.get_template('matches/index.html')
	c = Context({
		'latest_matches_list': latest_matches_list,
	})
	return HttpResponse(t.render(c))

def detail(request, matches_id):
	return HttpResponse("You're looking at match %s." % matches_id)

def results(request, matches_id):
	return HttpResponse("You're using match %s." % matches_id)


#def searchresults(request, search_id):

