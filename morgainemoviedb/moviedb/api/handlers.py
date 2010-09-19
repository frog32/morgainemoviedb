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
from django.contrib.auth import authenticate, login, logout
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
            'default',
            'country',
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
            'image_thumb',
            'image_original',
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
        result = m.setIMDB(request.PUT.get('imdbID'))
        if result == []:
            return rc.ALL_OK
        else:
            resp = HttpResponse(
                simplejson.dumps(result)
            )
            resp.status_code = 400
            return resp
            
    
    
    

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
            'country',
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

    
class UserAuthenticateHandler(BaseHandler):
    allowed_methods = ('GET', 'POST', 'DELETE')
    model = User
    fields = (
        'id',
        'username',
    )

    def read(self, request):
        if request.user.is_authenticated():
            return request.user
        else:
            return False
    
    def create(self, request):
        user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
        if user is not None:
            if user.is_active:
                login(request, user)
                return user
            else:
                # Return a 'disabled account' error message
                return False
        else:
            # Return an 'invalid login' error message.
            return False
    
    def delete(self, request):
        logout(request)
        return False
        

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
    
