import urllib2
import json
import os

from moviedb.models import Genre, Person, Country, Job, Poster, Title

config = {}
config['apikey'] = "a470dddae9a3fb7db6791108133cea05"
config['language'] = "en"
config['urls'] = {}
config['urls']['movie.search'] = "http://api.themoviedb.org/2.1/Movie.search/%(language)s/json/%(apikey)s/%%(query)s" % (config)
config['urls']['movie.getInfo'] = "http://api.themoviedb.org/2.1/Movie.getInfo/%(language)s/json/%(apikey)s/%%(movie_id)s" % (config)
config['urls']['media.getInfo'] = "http://api.themoviedb.org/2.1/Media.getInfo/%(language)s/json/%(apikey)s/%%(hash)s/%%(size)s" % (config)

def set_movie(movie, tmdb_id):
    result = _tmdb_get_data('movie.getInfo', {'movie_id':tmdb_id})[0]
    #set movie data
    movie.tmdb_id = result['id']
    movie.imdb_id = result['imdb_id']
    movie.year = result['released'][0:4]
    movie.tmdb_version = result['version']

    # insert titles
    movie.titles.all().delete()
    movie.titles.add(Title(text = result['name'], language = u'Original', default=True))

    # insert genres
    movie.genres = []
    for genre in result['genres']:
        movie.genres.add(search_or_add_genre(genre))
    # insert countries
    movie.countries = []
    for country in result['countries']:
        movie.countries.add(search_or_add_country(country))
    # insert cast
    movie.cast.all().delete()
    for job in result['cast']:
        person = search_or_add_person(job)
        Job.objects.create(character=job['character'], department=job['department'], movie=movie, person=person)
    # get image data from themoviedb
    available_posters = (poster.tmdb_id for poster in movie.posters.all())
    for poster in result['posters']:
        if poster['image']['size']!='original':
            continue
        if poster['image']['id'] in available_posters:
            continue
        newPoster = Poster(remote_path = poster['image']['url'], source_type = u'themoviedb', tmdb_id=poster['image']['id'])
        print 'here 1'
        try:
            newPoster.download()
            newPoster.generate_thumb()
            movie.posters.add(newPoster)
        except:
            raise
            print "couldn't load this image"
    movie.save()

def search_movies(query):
    results = _tmdb_get_data('movie.search', {'query':urllib2.quote(query)})
    if type(results[0]) != type({}):
        return []
    response = []
    for m in results:
        response.append({'id':m['id'], 'title':m['name'], 'year':m['released'][0:4], 'link':m['url']})
    return response
    
def lookup_hash(movie):
    for file in movie.files.all():
        if file.type == 'movie':
            result = _tmdb_get_data('media.getInfo', {'hash':file.hash,'size':file.size})
            print result
            if not result[0] == 'Nothing found.':
                if len(result)>1:
                    return False
                set_movie(movie,result[0]['id'])
                return True
            else:
                return False

def _tmdb_get_data(action, params):
    req = urllib2.Request(config['urls'][action] % params)
    req.add_header('User-Agent', 'Mozilla/5.0 (%s; en-GB; rv:1.9.0.3) urllib2 python' % (os.name))
    response = urllib2.urlopen(req)
    content=response.read()
    response.close()
    return json.loads(content)

# search or add functions
def search_or_add_country(country):
    query=Country.objects.filter(code=country['code'])
    if query.count():
        return query[0]
    else:
        return Country.objects.create(code=country['code'], name=country['name'])
        
def search_or_add_person(job):
    query=Person.objects.filter(tmdb_id = job['id'])
    if query.count():
        return query[0]
    else:
        return Person.objects.create(tmdb_id = job['id'], name = job['name'])

def search_or_add_genre(genre):
    query=Genre.objects.filter(name = genre['name'])
    if query.count():
        return query[0]
    else:
        return Genre.objects.create(name = genre['name'], tmdb_id=genre['id'])
