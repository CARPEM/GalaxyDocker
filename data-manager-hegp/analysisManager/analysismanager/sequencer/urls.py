from django.conf.urls import url

from . import views
app_name = 'protonprojects'
urlpatterns = [
    url(r'^$', views.showSavedData, name='savedData'),
    #~ url(r'^$', views.getExperiments, name='projects'),
    url(r'^actualize/$', views.actualize, name='actualize'),
    url(r'^downloads/actualize/$', views.actualizeDownloads, name='actualizedownloads'),
    url(r'^getBam/(?P<experiment_name>[-A-Za-z_0-9_.]+)$', views.getBamReviewed, name='getBam'),
    url(r'^getBamFromNgsData/(?P<experiment_name>[-A-Za-z_0-9_.]+)$', views.getBamFromNgsData, name='getBamNGS'),
    url(r'^getSequenceData/(?P<experiment_name>[-A-Za-z_0-9_.]+)$', views.getSequenceData, name='getSequenceData'),
    url(r'^actualizeusers/$', views.getGalaxyUsers, name='getgalaxyusers'),
    #~ url(r'^(?P<user_name>[-A-Za-z_0-9_.]+)$', views.getExperimentsLogs, name='projectslogs'),    
    url(r'^(?P<user_name>[-A-Za-z_0-9_.]+)$', views.showSavedDataLogs, name='showdatalogs'),    
    url(r'^(?P<user_id>[-A-Za-z_0-9_.]+)/vote/$', views.vote, name='vote'),
    url(r'^downloads/$', views.downloads, name='downloadsdata'),
    #~ url(r'^savedData/$', views.showSavedData, name='savedData'),



]   
