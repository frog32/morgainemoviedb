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
