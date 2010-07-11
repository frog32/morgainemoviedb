from django.conf.urls.defaults import *
from piston.resource import Resource
from moviedb.api.handlers import MovieHandler, MovieListHandler, MovieBookmarkHandler, UserAuthstateHandler, ImdbSearchHandler

movie_handler = Resource(MovieHandler)
movie_list_handler = Resource(MovieListHandler)
movie_bookmark_handler = Resource(MovieBookmarkHandler)

user_authstate_handler = Resource(UserAuthstateHandler)

imdb_search_handler = Resource(ImdbSearchHandler)

urlpatterns = patterns('',
    url(r'^movies\.(?P<emitter_format>.+)$', movie_list_handler, name = 'mdb_movies_list'),
    url(r'^movies/(?P<id>\d+)\.(?P<emitter_format>.+)$', movie_handler, name = 'mdb_movies'),
    url(r'^movies/(?P<id>\d+)/bookmark\.(?P<emitter_format>.+)$', movie_bookmark_handler, name = 'mdb_movies_bookmark'),

    url(r'^users/authstate\.(?P<emitter_format>.+)$', user_authstate_handler, name = 'mdb_users_authstate'),

    url(r'^imdb/search/(?P<query>.+)\.(?P<emitter_format>[^.]+)$', imdb_search_handler, name = 'mdb_imdb_search')
   
)
