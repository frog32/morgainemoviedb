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

from moviedb.models import Movie, Title, Genre, Person, Job, Country, Poster, File, AudioTrack, VideoTrack, SubtitleTrack, Folder
from moviedb.forms_admin import FileImportForm
from django.contrib import admin
from django.conf.urls.defaults import patterns
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from moviedb.conf import settings

from xml.etree import ElementTree


import threading

from moviedb.scrappers import ScrapperClient
scrapper = ScrapperClient()
scrapper.set_scrapper(settings.SCRAPPER)


class PosterAdmin(admin.ModelAdmin):
    #exclude = ('image_thumb',)
    pass

def scan_folders(modeladmin, request, queryset):
    class FolderScaner(threading.Thread):
        """Thread to scan all Folders"""

        def run(self):
            for obj in queryset:
                obj.scan()
    
    s=FolderScaner()
    s.start()

scan_folders.short_description = "Scan these Folders for new Movies"

class FolderAdmin(admin.ModelAdmin):
    actions = [scan_folders]

class VideoTrackAdmin(admin.TabularInline):
    model = VideoTrack
    extra = 0

class AudioTrackAdmin(admin.TabularInline):
    model = AudioTrack
    extra = 0

class SubtitleTrackAdmin(admin.TabularInline):
    model = SubtitleTrack
    extra = 0

class FileAdmin(admin.ModelAdmin):
    inlines = [
        VideoTrackAdmin,
        AudioTrackAdmin,
        SubtitleTrackAdmin,
    ]
    
class TitleAdmin(admin.TabularInline):
    model = Title
    extra = 0
    
class MovieAdmin(admin.ModelAdmin):
    inlines = [
        TitleAdmin,
    ]
    list_display = ('default_title', 'year',)
    filter_horizontal = ('genres', 'countries')
    search_fields = ('titles__text',)

    def import_xml_view(self, request):
        if request.method == 'POST':
            form = FileImportForm(request.POST, request.FILES)
            if form.is_valid():
                tree = ElementTree.parse(form.cleaned_data['import_field'])
                xml_movies = tree.getroot().getchildren()
                if request.POST.has_key("_send_identification"):
                    output = []
                    for xml_movie in xml_movies:
                        if xml_movie.find('tmdb_id') is None or xml_movie.find('tmdb_id').text is None:
                            continue                        
                        for xml_file in xml_movie.find('movie_files').getchildren():
                            filequery = File.objects.media_search(xml_file.find('hash').text, xml_file.find('size').text)
                            if filequery.count() == 1:
                                movie = filequery.get().movie
                                if movie.tmdb_id != 0:
                                    continue
                                if scrapper.set_movie(movie, int(xml_movie.find('tmdb_id').text)):
                                    output.append("Set movie %s" % (movie.default_title(),))
                                else:
                                    output.append("Error setting %s to movie %s" % (xml_movie.find('tmdb_id').text, movie.id))
                    return render_to_response('admin/moviedb/movie/identification_import.html',
                        {'output':output})
                return render_to_response('admin/moviedb/movie/compare.html')
        form = FileImportForm()
        context = {
            'adminform':form
        }
        context.update(csrf(request))
        return render_to_response('admin/moviedb/movie/import_xml.html', context)
        
    def get_urls(self):
        urls = super(MovieAdmin, self).get_urls()
        my_urls = patterns('',
            (r'^import_xml/$', self.admin_site.admin_view(self.import_xml_view))
        )
        return my_urls + urls

class PersonAdmin(admin.ModelAdmin):
    list_display = ('name',)
    
admin.site.register(Movie, MovieAdmin)
admin.site.register(Genre)
admin.site.register(Person, PersonAdmin)
admin.site.register(Job)
admin.site.register(Country)
admin.site.register(Poster, PosterAdmin)
admin.site.register(File,FileAdmin)
admin.site.register(Folder, FolderAdmin)
