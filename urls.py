from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'crabbetter.views.home', name='home'),
    # url(r'^crabbetter/', include('crabbetter.foo.urls')),
    url(r'^parsetwit/$', 'parsetwit.views.index'),
    url(r'^parsetwit/(?P<parsetwit_id>\d+)/$', 'parsetwit.views.detail'),
    url(r'^parsetwit/(?P<parsetwit_id>\d+)/results/$','parsetwit.views.detail'),
    #url(r'^parsetwit/search/(?P<search_id>\d+)/$', 'parsetwit.views.searchresults'),
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
