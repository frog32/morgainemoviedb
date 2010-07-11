from django.conf.urls.defaults import *
from morgainemoviedb import views, settings
from django.contrib import admin


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls), name = 'admin'),
    url(r'^mdb/', include('morgainemoviedb.moviedb.urls'), name = 'mdb'),
    url(r'^index\.html$', views.index),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes': True})
    
)
