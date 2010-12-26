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
from moviedb.conf import settings
from moviedb.models import Movie, MovieList, MovieExport, MovieXBMC
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from moviedb.scrappers import ScrapperClient

scrapper = ScrapperClient()
scrapper.set_scrapper(settings.SCRAPPER)

class DjangoAuthentication(object):
    """
    Django authentication. 
    """    
    def is_authenticated(self, request):
        return request.user.is_authenticated()
        
    def challenge(self):
        return rc.FORBIDDEN

class MovieHandler(BaseHandler):
    allowed_methods = ('GET', 'PUT',)
    model = Movie
    fields = (
        'id',
        'year',
        'imdb_id',
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
        ('cast',(
            'id',
            'character',
            'department',
            ('person',(
                'id',
                'name',
            )),
        )),
        ('posters',(
            'id',
            'image_thumb',
            'image_original',
        )),
        ('files',(
            'name',
            'path',
            'hash',
            'size',
            'type',
            ('video_tracks',(
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
        scrapper.set_movie(m, request.PUT.get('id'))
#        if result == []:
        return rc.ALL_OK
        # else:
            # resp = HttpResponse(
            #     simplejson.dumps(result)
            # )
            # resp.status_code = 400
            # return resp
            
    
    
    

class MovieListHandler(BaseHandler):
    allowed_methods = ('GET',)
    model = MovieList
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
        return MovieList.objects.all()
        
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
        

class MovieLookupHandler(BaseHandler):
    allowed_methods = ('GET',)
    
    def read(self, request, query):
        return scrapper.search_movies(query)

class MovieExportHandler(BaseHandler):
    allowed_methods = ('GET',)
    model = MovieExport
    fields = (
        'tmdb_id',
        'imdb_id',
        'resolution',
        'duration',
        ('movie_files', ( 'hash', 'format', 'format', 'size')),
        ('titles', ('text', 'default', 'country',)),
    )
    
    def read(self, request):
        return MovieExport.objects.filter(active=True)
        

class XBMCListHandler(BaseHandler):
    allowed_methods = ('GET',)
    model = MovieXBMC
    fields = (
        'id',
        'year',
        ('genres',(
            'name',
        )),
        'default_title',
        'default_poster',
        'file_path',
        ('countries',(
            'name',
        )),
        'languages',
        'duration',
    )

    def read(self,request):
        return MovieXBMC.objects.all()
