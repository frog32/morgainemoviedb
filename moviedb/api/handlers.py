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
    
