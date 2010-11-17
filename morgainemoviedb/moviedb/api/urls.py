# morgainemoviedb -- a tool to organize your local movies
# Copyright 2010 Marc Egli
#
# This file is part of morgainemoviedb.
# 
# morgainemoviedb is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# morgainemoviedb is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
# 
# You should have received a copy of the GNU Affero General Public License
# along with morgainemoviedb.  If not, see <http://www.gnu.org/licenses/>.

from django.conf.urls.defaults import *
from piston.resource import Resource
from moviedb.api.handlers import MovieHandler, MovieListHandler,\
    MovieBookmarkHandler, UserAuthenticateHandler, MovieLookupHandler,\
    MovieExportHandler

movie_handler = Resource(MovieHandler)
movie_list_handler = Resource(MovieListHandler)
movie_bookmark_handler = Resource(MovieBookmarkHandler)

user_authenticate_hander = Resource(UserAuthenticateHandler)

movie_lookup_handler = Resource(MovieLookupHandler)

movie_export_handler = Resource(MovieExportHandler)

urlpatterns = patterns('',
    url(r'^movies\.(?P<emitter_format>.+)$', movie_list_handler, name = 'mdb.movies.list'),
    url(r'^movies/(?P<id>\d+)\.(?P<emitter_format>.+)$', movie_handler, name = 'mdb.movies'),
    url(r'^movies/(?P<id>\d+)/bookmark\.(?P<emitter_format>.+)$', movie_bookmark_handler, name = 'mdb.movies.bookmark'),
    url(r'^export/movies.(?P<emitter_format>.+)$', movie_export_handler, name = 'mdb.evport.movies'),

    url(r'^users/authenticate\.(?P<emitter_format>.+)$', user_authenticate_hander, name = 'mdb.users.authenticate'),

    url(r'^lookup/search/(?P<query>.+)\.(?P<emitter_format>[^.]+)$', movie_lookup_handler, name = 'mdb_lookup_search')
   
)
