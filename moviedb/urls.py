from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^api/', include('moviedb.api.urls'), name = 'mdb_api'),
    
)
