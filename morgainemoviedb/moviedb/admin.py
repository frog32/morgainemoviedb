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

from moviedb.models import Movie, Title, Genre, Person, Role, Actor, Country, Poster, File, AudioTrack, VideoTrack, SubtitleTrack, Folder

from django.contrib import admin

import threading

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

class AudioTrackAdmin(admin.TabularInline):
    model = AudioTrack

class SubtitleTrackAdmin(admin.TabularInline):
    model = SubtitleTrack

class FileAdmin(admin.ModelAdmin):
    inlines = [
        VideoTrackAdmin,
        AudioTrackAdmin,
        SubtitleTrackAdmin,
    ]
    
class TitleAdmin(admin.TabularInline):
    model = Title
    extra = 1
    
class MovieAdmin(admin.ModelAdmin):
    inlines = [
        TitleAdmin,
    ]
    list_display = ('default_title', 'year',)

class PersonAdmin(admin.ModelAdmin):
    list_display = ('name', 'imdb_id',)
    
admin.site.register(Movie, MovieAdmin)
admin.site.register(Genre)
admin.site.register(Person, PersonAdmin)
admin.site.register(Role)
admin.site.register(Actor)
admin.site.register(Country)
admin.site.register(Poster, PosterAdmin)
admin.site.register(File,FileAdmin)
admin.site.register(Folder, FolderAdmin)
admin.site.register(Title)
