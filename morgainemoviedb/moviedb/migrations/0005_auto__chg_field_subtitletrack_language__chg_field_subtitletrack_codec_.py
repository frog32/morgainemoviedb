# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'SubtitleTrack.language'
        db.alter_column('moviedb_subtitletrack', 'language', self.gf('django.db.models.fields.CharField')(max_length=5))

        # Changing field 'SubtitleTrack.codec'
        db.alter_column('moviedb_subtitletrack', 'codec', self.gf('django.db.models.fields.CharField')(max_length=20))

        # Changing field 'SubtitleTrack.name'
        db.alter_column('moviedb_subtitletrack', 'name', self.gf('django.db.models.fields.CharField')(max_length=30))

        # Changing field 'Genre.name'
        db.alter_column('moviedb_genre', 'name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=20))

        # Changing field 'AudioTrack.language'
        db.alter_column('moviedb_audiotrack', 'language', self.gf('django.db.models.fields.CharField')(max_length=5))

        # Changing field 'AudioTrack.channels'
        db.alter_column('moviedb_audiotrack', 'channels', self.gf('django.db.models.fields.CharField')(max_length=5))

        # Changing field 'AudioTrack.codec'
        db.alter_column('moviedb_audiotrack', 'codec', self.gf('django.db.models.fields.CharField')(max_length=20))

        # Changing field 'AudioTrack.name'
        db.alter_column('moviedb_audiotrack', 'name', self.gf('django.db.models.fields.CharField')(max_length=30))

        # Changing field 'Person.name'
        db.alter_column('moviedb_person', 'name', self.gf('django.db.models.fields.CharField')(max_length=100))

        # Changing field 'Role.name'
        db.alter_column('moviedb_role', 'name', self.gf('django.db.models.fields.CharField')(max_length=100))

        # Changing field 'File.hash'
        db.alter_column('moviedb_file', 'hash', self.gf('django.db.models.fields.CharField')(max_length=32, blank=True))

        # Changing field 'File.format'
        db.alter_column('moviedb_file', 'format', self.gf('django.db.models.fields.CharField')(max_length=20))

        # Changing field 'File.type'
        db.alter_column('moviedb_file', 'type', self.gf('django.db.models.fields.CharField')(max_length=20))

        # Changing field 'Title.comment'
        db.alter_column('moviedb_title', 'comment', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True))

        # Changing field 'Title.language'
        db.alter_column('moviedb_title', 'language', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True))

        # Changing field 'Title.country'
        db.alter_column('moviedb_title', 'country', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True))

        # Changing field 'Title.text'
        db.alter_column('moviedb_title', 'text', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'Poster.name'
        db.alter_column('moviedb_poster', 'name', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True))

        # Changing field 'VideoTrack.codec'
        db.alter_column('moviedb_videotrack', 'codec', self.gf('django.db.models.fields.CharField')(max_length=20))

        # Changing field 'VideoTrack.name'
        db.alter_column('moviedb_videotrack', 'name', self.gf('django.db.models.fields.CharField')(max_length=30))

        # Changing field 'Country.name'
        db.alter_column('moviedb_country', 'name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100))


    def backwards(self, orm):
        
        # Changing field 'SubtitleTrack.language'
        db.alter_column('moviedb_subtitletrack', 'language', self.gf('django.db.models.fields.TextField')(max_length=5))

        # Changing field 'SubtitleTrack.codec'
        db.alter_column('moviedb_subtitletrack', 'codec', self.gf('django.db.models.fields.TextField')(max_length=20))

        # Changing field 'SubtitleTrack.name'
        db.alter_column('moviedb_subtitletrack', 'name', self.gf('django.db.models.fields.TextField')(max_length=30))

        # Changing field 'Genre.name'
        db.alter_column('moviedb_genre', 'name', self.gf('django.db.models.fields.TextField')(max_length=20, unique=True))

        # Changing field 'AudioTrack.language'
        db.alter_column('moviedb_audiotrack', 'language', self.gf('django.db.models.fields.TextField')(max_length=5))

        # Changing field 'AudioTrack.channels'
        db.alter_column('moviedb_audiotrack', 'channels', self.gf('django.db.models.fields.TextField')(max_length=5))

        # Changing field 'AudioTrack.codec'
        db.alter_column('moviedb_audiotrack', 'codec', self.gf('django.db.models.fields.TextField')(max_length=20))

        # Changing field 'AudioTrack.name'
        db.alter_column('moviedb_audiotrack', 'name', self.gf('django.db.models.fields.TextField')(max_length=30))

        # Changing field 'Person.name'
        db.alter_column('moviedb_person', 'name', self.gf('django.db.models.fields.TextField')())

        # Changing field 'Role.name'
        db.alter_column('moviedb_role', 'name', self.gf('django.db.models.fields.TextField')(max_length=30))

        # Changing field 'File.hash'
        db.alter_column('moviedb_file', 'hash', self.gf('django.db.models.fields.TextField')(blank=True))

        # Changing field 'File.format'
        db.alter_column('moviedb_file', 'format', self.gf('django.db.models.fields.TextField')(max_length=20))

        # Changing field 'File.type'
        db.alter_column('moviedb_file', 'type', self.gf('django.db.models.fields.TextField')(max_length=20))

        # Changing field 'Title.comment'
        db.alter_column('moviedb_title', 'comment', self.gf('django.db.models.fields.TextField')(max_length=100, blank=True))

        # Changing field 'Title.language'
        db.alter_column('moviedb_title', 'language', self.gf('django.db.models.fields.TextField')(max_length=30, blank=True))

        # Changing field 'Title.country'
        db.alter_column('moviedb_title', 'country', self.gf('django.db.models.fields.TextField')(max_length=30, blank=True))

        # Changing field 'Title.text'
        db.alter_column('moviedb_title', 'text', self.gf('django.db.models.fields.TextField')())

        # Changing field 'Poster.name'
        db.alter_column('moviedb_poster', 'name', self.gf('django.db.models.fields.TextField')(max_length=200, blank=True))

        # Changing field 'VideoTrack.codec'
        db.alter_column('moviedb_videotrack', 'codec', self.gf('django.db.models.fields.TextField')(max_length=20))

        # Changing field 'VideoTrack.name'
        db.alter_column('moviedb_videotrack', 'name', self.gf('django.db.models.fields.TextField')(max_length=30))

        # Changing field 'Country.name'
        db.alter_column('moviedb_country', 'name', self.gf('django.db.models.fields.TextField')(max_length=30, unique=True))


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'moviedb.actor': {
            'Meta': {'object_name': 'Actor'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'movie': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'actors'", 'to': "orm['moviedb.Movie']"}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['moviedb.Person']"}),
            'role': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['moviedb.Role']"})
        },
        'moviedb.audiotrack': {
            'Meta': {'object_name': 'AudioTrack'},
            'bitrate': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'channels': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'codec': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'default': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'file': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'audioTracks'", 'to': "orm['moviedb.File']"}),
            'forced': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'uid': ('django.db.models.fields.IntegerField', [], {})
        },
        'moviedb.bookmark': {
            'Meta': {'object_name': 'Bookmark'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'movie': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'bookmarks'", 'to': "orm['moviedb.Movie']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'bookmarks'", 'to': "orm['auth.User']"})
        },
        'moviedb.comment': {
            'Meta': {'object_name': 'Comment'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'movie': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'comments'", 'to': "orm['moviedb.Movie']"}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'comments'", 'to': "orm['auth.User']"})
        },
        'moviedb.country': {
            'Meta': {'object_name': 'Country'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        'moviedb.file': {
            'Meta': {'object_name': 'File'},
            'duration': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'folder': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'files'", 'to': "orm['moviedb.Folder']"}),
            'format': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'hash': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'movie': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'files'", 'null': 'True', 'to': "orm['moviedb.Movie']"}),
            'name': ('django.db.models.fields.TextField', [], {}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'childs'", 'null': 'True', 'to': "orm['moviedb.File']"}),
            'path': ('django.db.models.fields.TextField', [], {}),
            'size': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'moviedb.folder': {
            'Meta': {'object_name': 'Folder'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'path': ('django.db.models.fields.TextField', [], {}),
            'scanMode': ('django.db.models.fields.IntegerField', [], {}),
            'type': ('django.db.models.fields.IntegerField', [], {})
        },
        'moviedb.genre': {
            'Meta': {'object_name': 'Genre'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'})
        },
        'moviedb.movie': {
            'Meta': {'object_name': 'Movie'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'bookmarkedMovies': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'bookmarkedUsers'", 'blank': 'True', 'through': "orm['moviedb.Bookmark']", 'to': "orm['auth.User']"}),
            'cast': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['moviedb.Person']", 'symmetrical': 'False', 'through': "orm['moviedb.Actor']", 'blank': 'True'}),
            'countries': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'movies'", 'blank': 'True', 'to': "orm['moviedb.Country']"}),
            'directors': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'moviesDirector'", 'blank': 'True', 'db_table': "'moviedb_movie_directors'", 'to': "orm['moviedb.Person']"}),
            'duration': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'genres': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'movies'", 'blank': 'True', 'to': "orm['moviedb.Genre']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imdbID': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'languages': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'mdbID': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'resolution': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'writers': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'moviesWriter'", 'blank': 'True', 'db_table': "'moviedb_movie_writers'", 'to': "orm['moviedb.Person']"}),
            'year': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'moviedb.person': {
            'Meta': {'object_name': 'Person'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imdbID': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'moviedb.poster': {
            'Meta': {'object_name': 'Poster'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imageOriginal': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'imageThumb': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'movie': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'posters'", 'to': "orm['moviedb.Movie']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'remotePath': ('django.db.models.fields.TextField', [], {}),
            'sourceType': ('django.db.models.fields.TextField', [], {})
        },
        'moviedb.role': {
            'Meta': {'object_name': 'Role'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imdbID': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'moviedb.subtitletrack': {
            'Meta': {'object_name': 'SubtitleTrack'},
            'codec': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'default': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'file': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'subtitleTracks'", 'to': "orm['moviedb.File']"}),
            'forced': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'uid': ('django.db.models.fields.IntegerField', [], {})
        },
        'moviedb.title': {
            'Meta': {'object_name': 'Title'},
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'default': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'movie': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'titles'", 'to': "orm['moviedb.Movie']"}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'moviedb.videotrack': {
            'Meta': {'object_name': 'VideoTrack'},
            'bitrate': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'codec': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'default': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'file': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'videoTracks'", 'to': "orm['moviedb.File']"}),
            'forced': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'height': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'uid': ('django.db.models.fields.IntegerField', [], {}),
            'width': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['moviedb']
