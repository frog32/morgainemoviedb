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

from django.contrib import admin
from moviedb.models import Movie, Title, Genre, Person, Role, Actor, Country, Poster, File, AudioTrack, VideoTrack, SubtitleTrack, Folder

class PosterAdmin(admin.ModelAdmin):
    exclude = ('imageThumb',)

def scan_folders(modeladmin, request, queryset):
    for obj in queryset:
        obj.scan()
scan_folders.short_description = "Scan these Folders for new Movies"

class FolderAdmin(admin.ModelAdmin):
    actions = [scan_folders]

admin.site.register(Movie)
admin.site.register(Title)
admin.site.register(Genre)
admin.site.register(Person)
admin.site.register(Role)
admin.site.register(Actor)
admin.site.register(Country)
admin.site.register(Poster, PosterAdmin)
admin.site.register(File)
admin.site.register(AudioTrack)
admin.site.register(VideoTrack)
admin.site.register(SubtitleTrack)
admin.site.register(Folder, FolderAdmin)
