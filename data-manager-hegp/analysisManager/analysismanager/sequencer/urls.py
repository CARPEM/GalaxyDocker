from django.conf.urls import url

from . import views
app_name = 'protonprojects'
urlpatterns = [
    url(r'^$', views.getExperiments, name='projects'),
    url(r'^actualize/$', views.actualize, name='actualize'),
    url(r'^getBam/(?P<experiment_name>[-A-Za-z_0-9_.]+)$', views.getBamReviewed, name='getBam'),
    url(r'^actualizeusers/$', views.getGalaxyUsers, name='getgalaxyusers'),
    url(r'^(?P<user_name>[-A-Za-z_0-9_.]+)$', views.getExperimentsLogs, name='projectslogs'),    
    url(r'^(?P<user_id>[-A-Za-z_0-9_.]+)/vote/$', views.vote, name='vote'),



]   
