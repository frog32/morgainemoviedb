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

from moviedb.conf import settings
from moviedb.utils import *
from django.db import models
from django.utils.encoding import force_unicode
from django.contrib.auth.models import User
import os
import subprocess
import re
import urllib2
import Image
import imdb

class Movie(models.Model):
    """representing a movie"""
    year = models.IntegerField(default=0)
    imdbID = models.IntegerField(default=0)
    mdbID = models.IntegerField(default=0)
    active = models.BooleanField(default=True)

    duration = models.IntegerField(default=0)
    languages = models.TextField(blank=True)
    resolution = models.CharField(blank=True, max_length=20)

    genres = models.ManyToManyField('Genre', related_name = 'movies', blank=True)
    writers = models.ManyToManyField('Person', related_name = 'moviesWriter', db_table = 'moviedb_movie_writers', blank=True)
    directors = models.ManyToManyField('Person', related_name = 'moviesDirector', db_table = 'moviedb_movie_directors', blank=True)
    cast = models.ManyToManyField('Person', through = 'Actor', blank=True)
    countries = models.ManyToManyField('Country', related_name = 'movies', blank=True)
    
    bookmarkedMovies = models.ManyToManyField(User, related_name = 'bookmarkedUsers', blank=True, through = 'Bookmark')
    #files = OneToMany('File')
    #posters = OneToMany('Poster')
    #comments = OneToMany('Comment')

    def __repr__(self):
        if self.id:
            return '<Movie "%d">' % (self.id,)
        else:
            return '<Movie "unsaved">'

    def __unicode__(self):
        return self.default_title()

    def default_title(self):
        t = Title.objects.filter(movie__id = self.id).filter(default=True)
        if t.count():
            return t.get().text
        else:
            return u'New Movie'
    default_title.short_description = u'Original Title'


    def setIMDB(self, imdbID):
        '''set imdbID and get all the information out of imdb'''
        m=imdb.IMDb(accessSystem='http', adultSearch=0).get_movie(imdbID)
        self.imdbID=int(imdbID)
        self.year=m['year']
        # insert titles
        for title in self.titles.all():
            title.delete()
        self.titles.add(Title(text = m['title'], language = u'Original'))
        for aka in m['akas']:
            result=re.match('^(.*?)::\(([^)]+)\) +(\(([^)]*)\) +)?\[([a-z]{2})\]', aka, re.IGNORECASE)
            if result:
                newTitle = Title(text = result.group(1), country = result.group(2), comment = result.group(4), language = result.group(5))
                newTitle.save()
                self.titles.add(newTitle)

        # insert genres
        self.genres=[]
        for gen in m['genres']:
                self.genres.add(searchOrAddGenre(gen))
        # insert countries
        self.countries=[]
        for country in m['countries']:
            query = Country.objects.filter(name = country)
            if query.count():
                self.countries.add(query[0])
            else:
                newCountry = Country(name = country)
                newCountry.save()
                self.countries.add(newCountry)
        # insert cast
        for actor in self.actors.all():
            actor.delete()
        if 'cast' in m.keys():
            for person in m['cast']:
                newPerson = searchOrAddPerson(person)
                if hasattr(person.currentRole,'__iter__'):
                    for role in person.currentRole:
                        # there are multiple roles for the same person
                        newRole = searchOrAddRole(role)
                        Actor.objects.create(role = newRole, person = newPerson, movie = self)
                else:
                    # this person only plays one role
                    if 'name' in person.currentRole.keys():
                        newRole = searchOrAddRole(person.currentRole)
                        Actor.objects.create(role = newRole, person = newPerson, movie = self)
                    else:
                        newRole = Role.objects.create(name = person['name'], imdbID = 0)
                        Actor.objects.create(role = newRole, person = newPerson, movie = self)

        # insert writers
        self.writers = []
        if hasattr(m['writer'],'__iter__'):
            for person in m['writer']:
                self.writers.add(searchOrAddPerson(person))
        else:
            person = m['writer']
            self.writers.add(searchOrAddPerson(person))
            
        # insert directors
        self.directors=[]
        if hasattr(m['director'],'__iter__'):
            for person in m['director']:
                self.directors.add(searchOrAddPerson(person))
        else:
            person = m['director']
            self.directors.add(searchOrAddPerson(person))

        # get image data from themoviedb
        self.posters=[]
        obj=themoviedb.getImages(self.imdbID)
        if obj[0] != 'Nothing found.':
            for poster in obj[0]['posters']:
                if poster['image']['size']=='original':
                    newPoster = Poster.objects.create(remotePath = poster['image']['url'], sourceType = u'themoviedb')
                    newPoster.download()
                    self.posters.add(newPoster)


    def searchOSHash(self):
        '''Checks if os hash matches an entry on themoviedb'''
        for file in self.files:
            if file.type == 'movie':
                result=themoviedb.lookupOSHash(file.hash)
                if not result[0] == 'Nothing found.':
                    if len(result)>1:
                        #print '###multiple results###'
                        #print result
                        return 'multiple results'
                    self.setIMDB(result[0]['imdb_id'][2:])
                    return 'Found Match for '+result[0]['name']
                else:
                    return 'No Match found'
    
    def save(self, **kwargs):
        self.update()
        super(Movie,self).save(**kwargs)
    
    def update(self):
        languages =[]
        self.duration = 0
        for file in self.files.all():
            self.duration = self.duration + file.duration
            if file.type == 'movie':
                for audioTrack in file.audioTracks.all():
                    if audioTrack.language != 'None' and not audioTrack.language in languages:
                        languages.append(audioTrack.language)
                self.resolution = file.getVideoFormat()
        self.languages = u','.join(languages)
    

    

class Title(models.Model):
    """a movie title"""
    text = models.CharField(max_length=255)
    country = models.CharField(max_length=30, blank=True)
    language = models.CharField(max_length=30, blank=True)
    comment = models.CharField(max_length=100, blank=True)
    default = models.BooleanField(default=False)

    movie = models.ForeignKey('Movie', related_name = 'titles')

    def __repr__(self):
      return '<Title "%s" (%s)>' % (self.text, self.country)

    def __unicode__(self):
        return self.text


def searchOrAddGenre(genre):
    query=Genre.objects.filter(name = genre)
    if query.count():
        return query[0]
    else:
        return Genre.objects.create(name = genre)

class Genre(models.Model):
    """genre of a movie"""
    name = models.CharField(max_length=20, unique=True)
    # movies manytomany

    def __repr__(self):
      return '<Genre "%s">' % (self.name,)

    def __unicode__(self):
        return self.name

def searchOrAddPerson(person):
    query=Person.objects.filter(imdbID = person.getID())
    if query.count():
        return query[0]
    else:
        return Person.objects.create(imdbID = person.getID(), name = person['name'])
    

class Person(models.Model):
    """a real person"""
    name = models.CharField(max_length=100)
    imdbID = models.IntegerField(default=0)

    #moviesWriter = ManyToMany('Movie', tablename = 'movie_writers')
    #moviesDirector = ManyToMany('Movie', tablename = 'movie_directors')
    #roles = OneToMany('Role')
    def __repr__(self):
        return '<Person "%s" (%d)>' % (self.name, self.imdbID)
        
    def __unicode__(self):
        return self.name


def searchOrAddRole(role):
    query=Role.objects.filter(imdbID = role.getID() if role.getID() != '' else 0).exclude(imdbID = 0)
    if query.count():
        return query[0]
    else:
        return Role.objects.create(imdbID = role.getID() if role.getID() else 0, name = role['name'])

class Role(models.Model):
    name = models.CharField(max_length=100)
    imdbID = models.IntegerField(default=0)

    def __repr__(self):
        if self.imdbID:
            return '<Role "%s" (%d)>' % (self.name, self.imdbID)
        return '<Role "%s" (null)>' % (self.name,)
    
    def __unicode__(self):
        return self.name
            

class Actor(models.Model):
    movie = models.ForeignKey('Movie', related_name = 'actors')
    person = models.ForeignKey('Person')
    role = models.ForeignKey('Role')
    
    def __unicode__(self):
        return '%s is playing %s in %s' % (self.person.name, self.role.name, self.movie.id)
        

class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    def __repr__(self):
        return '<Country "%s">' % (self.name,)
        
    def __unicode__(self):
        return self.name

#
class Poster(models.Model):
    """a poster belongs to a movie"""
    name = models.CharField(max_length=255, blank=True)
    remotePath = models.TextField()
    sourceType = models.TextField()
    order = models.IntegerField(default=0)
    imageOriginal = models.ImageField(upload_to = 'posters/original', blank=True)
    imageThumb = models.ImageField(upload_to = 'posters/thumb', blank=True)

    movie = models.ForeignKey('Movie', related_name = 'posters')

    def __repr__(self):
        return '<Poster "%s">' % (self.name,)
    
    def __unicode__(self):
        return self.name
    
    def save(self, **kwargs):
        super(Poster, self).save(**kwargs)
        im=Image.open(self.imageOriginal.path)
        thumbX=300
        thumbY=300
        im.thumbnail((thumbX, thumbY), Image.ANTIALIAS)
        self.imageThumb='posters/thumb/%d.jpg' % self.id
        #print self.imageThumb.path
        im.save(self.imageThumb.path)
        super(Poster, self).save(**kwargs)
        
    def download(self):
        pass
        


class File(models.Model):
    """representing a file"""
    path = models.TextField()
    name = models.TextField()
    type = models.CharField(max_length=20)
    format = models.CharField(max_length=20)
    hash = models.CharField(max_length=32, blank=True)
    size = models.IntegerField(default=0)
    duration = models.IntegerField(default=0)

    movie = models.ForeignKey('Movie', related_name = 'files', blank=True, null = True)
    folder = models.ForeignKey('Folder', related_name = 'files')
    #videoTracks = OneToMany('VideoTrack')
    #audioTracks = OneToMany('AudioTrack')
    #subtitleTracks = OneToMany('SubtitleTrack')
    parent = models.ForeignKey('self', related_name = 'childs', blank=True, null = True)

    def __repr__(self):
        return '<File "%s" (%s)>' % (self.name, self.path)
    
    def __unicode__(self):
        return self.path

    def getFileInfo(self):
        self.size=os.path.getsize(self.path)
        self.name=os.path.split(self.path)[1]
        if os.path.isdir(self.path):
            self.type = u'dir'
        elif os.path.splitext(self.name)[1] in settings.MOVIE_FILE_SUFFIXES.keys() and settings.MOVIE_FILE_SUFFIXES[os.path.splitext(self.name)[1]] == 'movie':
            self.type = u'movie'
            self.save()
            self.getTracks()
        else:
            self.type = u'unknown'
        if not self.type == u'dir':
            self.hash=unicode(opensubtitles.hashFile(self.path))

    def getTracks(self):
        '''get metadata with ffmpeg'''
        ffmpeginfo=subprocess.Popen(['ffmpeg', '-i', self.path], stderr=subprocess.PIPE).communicate()[1]

        result=re.search('(?<=Input #0, )[^,]+',ffmpeginfo)
        if result:
            self.format= result.group(0) 
        streams=re.findall('Stream #[0-9]\.[0-9].*$',ffmpeginfo,re.MULTILINE)
        for stream in streams:
            #print stream
            if re.match('Stream #0.([0-9]+)(\([a-z]{3}\))?: Video:',stream):
                #print 'video'
                result=re.match('Stream #0.([0-9]+)(\([a-z]{3}\))?: Video: ([a-z0-9]+), [a-z0-9]+, ([0-9]+)x([0-9]+)', stream, re.IGNORECASE)
                self.videoTracks.add(VideoTrack(\
                        uid = result.group(1),\
                        codec = unicode(result.group(3)),\
                        width = result.group(4),\
                        height = result.group(5)))
            if re.match('Stream #0.([0-9]+)(\([a-z]{3}\))?: Audio:',stream):
                #print 'audio'
                stream=stream.replace('stereo','2.0')
                result=re.match('Stream #0.([0-9]+)(\(([a-z]{3})\))?: Audio: ([a-z0-9]+), [0-9]+ Hz, ([0-9]+\.?[0-9]*)', stream, re.IGNORECASE)
                self.audioTracks.add(
                    AudioTrack(
                        uid = result.group(1),
                        language = unicode(result.group(3)),
                        codec = unicode(result.group(4)),
                        channels = unicode(result.group(5)),
                        file = self
                    )
                )

    def scan(self, report):
        dirList=os.listdir(self.path)
        # add new files
        for entry in dirList:
            report['scan'] = report['scan'] + 1
            create=True
            for file in self.childs.all():
                if entry == file.name:
                    create=False
            for reg in settings.SCAN_EXCLUDE_FILES:
                if re.search(reg,entry):
                    create=False
            if create:
                newFile = File(path=os.path.join(self.path,entry), folder = self.folder)
                report['added'].append(newFile.path)
                newFile.getFileInfo()
                self.childs.add(newFile)
        # delete old files
        for file in self.childs.all():
            if not file.name in dirList:
                report['removed'].append(file.path)
                file.delete()
        # scan all subfolders
        for file in self.childs.all():
            if file.type == 'dir':
                report = file.scan(report)
        return report

    def setMovie(self,movie):
        self.movie = movie
        self.save()
        for child in self.childs.all():
            child.setMovie(movie)

    def containsMovies(self):
        if self.type == 'movie':
            return True
        for child in self.childs.all():
            if child.containsMovies():
                return True
        return False

    def getVideoFormat(self):
        smalestWidth=0
        for videoTrack in self.videoTracks.all():
            if videoTrack.width < smalestWidth or smalestWidth == 0:
                smalestWidth = videoTrack.width
            if smalestWidth >= 1920:
                return u'1080p'
            if smalestWidth >= 1280:
                return u'720p'
            if smalestWidth >= 800:
                return u'480p'
            return u'bad'


class VideoTrack(models.Model):
    """representing a video track"""
    name = models.CharField(max_length=30)
    default=models.BooleanField(default=False)
    forced = models.BooleanField(default=False)
    uid = models.IntegerField()
    codec = models.CharField(max_length=20)
    width = models.IntegerField()
    height = models.IntegerField()
    bitrate = models.IntegerField(default=0)

    file = models.ForeignKey('File', related_name = 'videoTracks')

    def __repr__(self):
        return '<VideoTrack %s (%dx%d)>' % (self.codec, self.width, self.height)
    

class AudioTrack(models.Model):
    """representing a audio track"""
    name = models.CharField(max_length=30)
    language = models.CharField(max_length=5)
    default=models.BooleanField(default=False)
    forced = models.BooleanField(default=False)
    uid = models.IntegerField()
    codec = models.CharField(max_length=20)
    channels = models.CharField(max_length=5)
    bitrate = models.IntegerField(default=0)

    file = models.ForeignKey('File', related_name = 'audioTracks')

    def __repr__(self):
        return '<AudioTrack %s (%s)>' % (self.codec, self.language)


class SubtitleTrack(models.Model):
    """representing a subtitle track"""
    name = models.CharField(max_length=30)
    language = models.CharField(max_length=5)
    default=models.BooleanField(default=False)
    forced = models.BooleanField(default=False)
    uid = models.IntegerField()
    codec = models.CharField(max_length=20)

    file = models.ForeignKey('File', related_name = 'subtitleTracks')

    def __repr__(self):
        return '<SubtitleTrack %s (%s)>' % (self.codec, self.language)



class Folder(models.Model):
    """a folder with different movies"""
    path = models.TextField()
    
    type = models.IntegerField(choices = settings.FOLDER_TYPE_CHOICES)
    scanMode = models.IntegerField(choices = settings.FOLDER_SCAN_MODE)
    
    #files = OneToMany('File')
    
    def __repr__(self):
        return '<Folder %s (%d)>' % (self.path, self.type)
    
    def __unicode__(self):
        return self.path
    
    def scan(self):
        dirList=os.listdir(self.path)
        # add new files
        report = {\
            'scan' : 0, \
            'added' : [], \
            'removed' : [], \
        }
        for entry in dirList:
            report['scan'] = report['scan'] + 1
            create=True
            for file in self.files.all():
                if entry == file.name:
                    create=False
                    if file.type == 'dir':
                        report = file.scan(report)
            for reg in settings.SCAN_EXCLUDE_FILES:
                if re.search(reg,entry):
                    create=False
            if create:
                newFile = File(path = os.path.join(self.path,entry), folder = self)
                report['added'].append(newFile.path)
                newFile.getFileInfo()
                self.files.add(newFile)
        # delete old files
        for file in self.files.all():
            if not file.name in dirList:
                report['removed'].append(file.path)
                file.delete()
        # scan all subfolders        
        for file in self.files.all():
            if file.type == 'dir':
                report = file.scan(report)
        # if not belongs to a movie assign it and all subfiles to a movie
        for file in self.files.filter(parent__isnull=True):
            if file.movie is None and file.containsMovies():
                newMovie = Movie()
                newMovie.save()
                file.setMovie(newMovie)
            
        return report


class Bookmark(models.Model):
    movie = models.ForeignKey('Movie', related_name = 'bookmarks')
    user = models.ForeignKey(User, related_name = 'bookmarks')
    
class Comment(models.Model):
    movie = models.ForeignKey('Movie', related_name = 'comments')
    user = models.ForeignKey(User, related_name = 'comments')
    text = models.TextField()