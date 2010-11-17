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
from moviedb import tmdb
from moviedb.opensubtitles import hash_file
from django.db import models
from django.utils.encoding import force_unicode
from django.contrib.auth.models import User
from django.core import files
import os
import subprocess
import re
import urllib2
import Image
import imdb

class Movie(models.Model):
    """representing a movie"""
    year = models.IntegerField(default=0)
    imdb_id = models.CharField(max_length=12, blank=True)
    tmdb_id = models.IntegerField(default=0)
    tmdb_version = models.IntegerField(default=0)
    active = models.BooleanField(default=True)

    duration = models.IntegerField(default=0)
    languages = models.TextField(blank=True)
    resolution = models.CharField(blank=True, max_length=20)

    genres = models.ManyToManyField('Genre', related_name = 'movies', blank=True)
    countries = models.ManyToManyField('Country', related_name = 'movies', blank=True)
    
    bookmarkedMovies = models.ManyToManyField(User, related_name = 'bookmarkedUsers', blank=True, through = 'Bookmark')
    
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
    
    def movie_files(self):
        return self.files.filter(type='movie')

    

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

class Genre(models.Model):
    """genre of a movie"""
    name = models.CharField(max_length=20, unique=True)
    tmdb_id = models.IntegerField(default=0)
    # movies manytomany

    def __repr__(self):
      return '<Genre "%s">' % (self.name,)

    def __unicode__(self):
        return self.name    

class Person(models.Model):
    """a real person"""
    name = models.CharField(max_length=100)
    tmdb_id = models.IntegerField(default=0)

    #moviesWriter = ManyToMany('Movie', tablename = 'movie_writers')
    #moviesDirector = ManyToMany('Movie', tablename = 'movie_directors')
    #roles = OneToMany('Role')
    def __repr__(self):
        return '<Person "%s" (%d)>' % (self.name, self.tmdb_id)
        
    def __unicode__(self):
        return self.name

class Job(models.Model):
    character = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    person = models.ForeignKey(Person)
    movie = models.ForeignKey(Movie, related_name='cast')
    
    class Meta:
        ordering = ('department',)
    def __repr__(self):
        return '<Job "%s">' % (self.name,)
    
    def __unicode__(self):
        return self.character        

class Country(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    
    def __repr__(self):
        return '<Country "%s">' % (self.name,)
        
    def __unicode__(self):
        return self.name

#
class Poster(models.Model):
    """a poster belongs to a movie"""
    name = models.CharField(max_length=255, blank=True)
    remote_path = models.TextField()
    source_type = models.TextField()
    order = models.IntegerField(default=0)
    image_original = models.ImageField(upload_to = 'posters/original', blank=True)
    image_thumb = models.ImageField(upload_to = 'posters/thumb', blank=True)
    tmdb_id = models.CharField(default='', max_length=25)

    movie = models.ForeignKey('Movie', related_name = 'posters')

    def __repr__(self):
        return '<Poster "%s">' % (self.name,)
    
    def __unicode__(self):
        return self.name
    
    def generate_thumb(self):
        im=Image.open(self.image_original.path)
        im.thumbnail((settings.POSTER_THUMBSIZE['x'], settings.POSTER_THUMBSIZE['y']), Image.ANTIALIAS)
        #print self.image_thumb.path
        img_temp = files.temp.NamedTemporaryFile(delete=True)
        im.save(img_temp,'jpeg')
        img_temp.flush()
        self.image_thumb.save(self.name, files.File(img_temp))
        self.save()
        
    def download(self):
        print self.remote_path
        self.name = os.path.split(self.remote_path)[1]
        download_temp = files.temp.NamedTemporaryFile(delete=True)
        download_temp.write(urllib2.urlopen(self.remote_path).read())
        download_temp.flush()
        self.image_original.save(self.name, files.File(download_temp))
        
        


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
    #video_tracks = OneToMany('VideoTrack')
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
            self.hash=unicode(hash_file(self.path))

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
                self.video_tracks.add(VideoTrack(\
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
        for video_track in self.video_tracks.all():
            if video_track.width < smalestWidth or smalestWidth == 0:
                smalestWidth = video_track.width
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

    file = models.ForeignKey('File', related_name = 'video_tracks')

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
        # todo: outsource this into a stragedy
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