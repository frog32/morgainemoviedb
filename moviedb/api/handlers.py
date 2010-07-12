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

from piston.handler import BaseHandler
from piston.utils import rc
from moviedb.models import Movie
from django.contrib.auth.models import User
import imdb

class MovieHandler(BaseHandler):
    allowed_methods = ('GET', 'PUT',)
    model = Movie
    fields = (
        'id',
        'year',
        'imdbID',
        ('genres',(
            'name',
        )),
        ('titles',(
            'text',
            'language',
        )),
        ('countries',(
            'name',
        )),
        ('writers',(
            'name',
            'imdbID',
        )),
        ('directors',(
            'name',
            'imdbID',
        )),
        ('actors',(
            ('person',(
                'name',
                'imdbID',
            )),
            ('role',(
                'name',
                'imdbID',
            )),
        )),
        ('posters',(
            'imageThumb',
            'imageOriginal',
        )),
        ('files',(
            'name',
            'hash',
            'size',
            'type',
            ('videoTracks',(
                'name',
                'codec',
                'width',
                'height',
            )),
            ('audioTracks',(
                'name',
                'codec',
                'language',
                'channels',
            )),
            ('subtitleTracks',(
                'name',
                'codec',
                'language',
            )),
        )),
        'duration',
        'resolution',
        
    )
    
    def update(self, request, id):
        m = Movie.objects.filter(id = id)[0]
        m.setIMDB(request.PUT.get('imdbID'))
        return rc.ALL_OK
    
    
    

class MovieListHandler(BaseHandler):
    allowed_methods = ('GET',)
    model = Movie
    fields = (
        'id',
        'year',
        ('genres',(
            'name',
        )),
        ('titles',(
            'text',
            'language',
        )),
        ('countries',(
            'name',
        )),
        'languages',
        'duration',
    )
    
    def read(self,request):
        return Movie.objects.all()
        
class MovieBookmarkHandler(BaseHandler):
    allowed_methods = ('POST')
    
    def write(self,request,movie_id):
        Movie.objects.filter(id = movie_id).one().bookmarkedUsers.add(User)
        return {'movie_id':movie_id}


class UserAuthstateHandler(BaseHandler):
    allowed_methods = ('GET',)
    model = User
    fields = (
        'id',
        'username',
    )

class ImdbSearchHandler(BaseHandler):
    allowed_methods = ('GET')
    
    def read(self, request, query):
        try:
            results = imdb.IMDb(accessSystem='http', adultSearch=0).search_movie(query)
            response=[]
            for m in results:
                response.append({'imdbID':m.movieID, 'title':m['title'], 'year':m['year']})
            return response
            
        except IOError:
            return 'IOError'
    
