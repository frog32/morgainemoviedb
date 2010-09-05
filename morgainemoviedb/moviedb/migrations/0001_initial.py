# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Movie'
        db.create_table('moviedb_movie', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('year', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('imdbID', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('mdbID', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True, blank=True)),
            ('duration', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('languages', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('resolution', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('moviedb', ['Movie'])

        # Adding M2M table for field genres on 'Movie'
        db.create_table('moviedb_movie_genres', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('movie', models.ForeignKey(orm['moviedb.movie'], null=False)),
            ('genre', models.ForeignKey(orm['moviedb.genre'], null=False))
        ))
        db.create_unique('moviedb_movie_genres', ['movie_id', 'genre_id'])

        # Adding M2M table for field writers on 'Movie'
        db.create_table('moviedb_movie_writers', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('movie', models.ForeignKey(orm['moviedb.movie'], null=False)),
            ('person', models.ForeignKey(orm['moviedb.person'], null=False))
        ))
        db.create_unique('moviedb_movie_writers', ['movie_id', 'person_id'])

        # Adding M2M table for field directors on 'Movie'
        db.create_table('moviedb_movie_directors', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('movie', models.ForeignKey(orm['moviedb.movie'], null=False)),
            ('person', models.ForeignKey(orm['moviedb.person'], null=False))
        ))
        db.create_unique('moviedb_movie_directors', ['movie_id', 'person_id'])

        # Adding M2M table for field countries on 'Movie'
        db.create_table('moviedb_movie_countries', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('movie', models.ForeignKey(orm['moviedb.movie'], null=False)),
            ('country', models.ForeignKey(orm['moviedb.country'], null=False))
        ))
        db.create_unique('moviedb_movie_countries', ['movie_id', 'country_id'])

        # Adding model 'Title'
        db.create_table('moviedb_title', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('country', self.gf('django.db.models.fields.TextField')(max_length=30, blank=True)),
            ('language', self.gf('django.db.models.fields.TextField')(max_length=30, blank=True)),
            ('comment', self.gf('django.db.models.fields.TextField')(max_length=100, blank=True)),
            ('default', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('movie', self.gf('django.db.models.fields.related.ForeignKey')(related_name='titles', to=orm['moviedb.Movie'])),
        ))
        db.send_create_signal('moviedb', ['Title'])

        # Adding model 'Genre'
        db.create_table('moviedb_genre', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.TextField')(unique=True, max_length=20)),
        ))
        db.send_create_signal('moviedb', ['Genre'])

        # Adding model 'Person'
        db.create_table('moviedb_person', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.TextField')()),
            ('imdbID', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('moviedb', ['Person'])

        # Adding model 'Role'
        db.create_table('moviedb_role', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.TextField')(max_length=30)),
            ('imdbID', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('moviedb', ['Role'])

        # Adding model 'Actor'
        db.create_table('moviedb_actor', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('movie', self.gf('django.db.models.fields.related.ForeignKey')(related_name='actors', to=orm['moviedb.Movie'])),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['moviedb.Person'])),
            ('role', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['moviedb.Role'])),
        ))
        db.send_create_signal('moviedb', ['Actor'])

        # Adding model 'Country'
        db.create_table('moviedb_country', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.TextField')(unique=True, max_length=30)),
        ))
        db.send_create_signal('moviedb', ['Country'])

        # Adding model 'Poster'
        db.create_table('moviedb_poster', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.TextField')(max_length=200)),
            ('remotePath', self.gf('django.db.models.fields.TextField')()),
            ('sourceType', self.gf('django.db.models.fields.TextField')()),
            ('order', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('imageOriginal', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('imageThumb', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('movie', self.gf('django.db.models.fields.related.ForeignKey')(related_name='posters', to=orm['moviedb.Movie'])),
        ))
        db.send_create_signal('moviedb', ['Poster'])

        # Adding model 'File'
        db.create_table('moviedb_file', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('path', self.gf('django.db.models.fields.TextField')()),
            ('name', self.gf('django.db.models.fields.TextField')()),
            ('type', self.gf('django.db.models.fields.TextField')(max_length=20)),
            ('format', self.gf('django.db.models.fields.TextField')(max_length=20)),
            ('hash', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('size', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('duration', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('movie', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='files', null=True, to=orm['moviedb.Movie'])),
            ('folder', self.gf('django.db.models.fields.related.ForeignKey')(related_name='files', to=orm['moviedb.Folder'])),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='childs', null=True, to=orm['moviedb.File'])),
        ))
        db.send_create_signal('moviedb', ['File'])

        # Adding model 'VideoTrack'
        db.create_table('moviedb_videotrack', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.TextField')(max_length=30)),
            ('default', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('forced', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('uid', self.gf('django.db.models.fields.IntegerField')()),
            ('codec', self.gf('django.db.models.fields.TextField')(max_length=20)),
            ('width', self.gf('django.db.models.fields.IntegerField')()),
            ('height', self.gf('django.db.models.fields.IntegerField')()),
            ('bitrate', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('file', self.gf('django.db.models.fields.related.ForeignKey')(related_name='videoTracks', to=orm['moviedb.File'])),
        ))
        db.send_create_signal('moviedb', ['VideoTrack'])

        # Adding model 'AudioTrack'
        db.create_table('moviedb_audiotrack', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.TextField')(max_length=30)),
            ('language', self.gf('django.db.models.fields.TextField')(max_length=5)),
            ('default', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('forced', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('uid', self.gf('django.db.models.fields.IntegerField')()),
            ('codec', self.gf('django.db.models.fields.TextField')(max_length=20)),
            ('channels', self.gf('django.db.models.fields.TextField')(max_length=5)),
            ('bitrate', self.gf('django.db.models.fields.IntegerField')()),
            ('file', self.gf('django.db.models.fields.related.ForeignKey')(related_name='audioTracks', to=orm['moviedb.File'])),
        ))
        db.send_create_signal('moviedb', ['AudioTrack'])

        # Adding model 'SubtitleTrack'
        db.create_table('moviedb_subtitletrack', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.TextField')(max_length=30)),
            ('language', self.gf('django.db.models.fields.TextField')(max_length=5)),
            ('default', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('forced', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('uid', self.gf('django.db.models.fields.IntegerField')()),
            ('codec', self.gf('django.db.models.fields.TextField')(max_length=20)),
            ('file', self.gf('django.db.models.fields.related.ForeignKey')(related_name='subtitleTracks', to=orm['moviedb.File'])),
        ))
        db.send_create_signal('moviedb', ['SubtitleTrack'])

        # Adding model 'Folder'
        db.create_table('moviedb_folder', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('path', self.gf('django.db.models.fields.TextField')()),
            ('type', self.gf('django.db.models.fields.IntegerField')()),
            ('scanMode', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('moviedb', ['Folder'])


    def backwards(self, orm):
        
        # Deleting model 'Movie'
        db.delete_table('moviedb_movie')

        # Removing M2M table for field genres on 'Movie'
        db.delete_table('moviedb_movie_genres')

        # Removing M2M table for field writers on 'Movie'
        db.delete_table('moviedb_movie_writers')

        # Removing M2M table for field directors on 'Movie'
        db.delete_table('moviedb_movie_directors')

        # Removing M2M table for field countries on 'Movie'
        db.delete_table('moviedb_movie_countries')

        # Deleting model 'Title'
        db.delete_table('moviedb_title')

        # Deleting model 'Genre'
        db.delete_table('moviedb_genre')

        # Deleting model 'Person'
        db.delete_table('moviedb_person')

        # Deleting model 'Role'
        db.delete_table('moviedb_role')

        # Deleting model 'Actor'
        db.delete_table('moviedb_actor')

        # Deleting model 'Country'
        db.delete_table('moviedb_country')

        # Deleting model 'Poster'
        db.delete_table('moviedb_poster')

        # Deleting model 'File'
        db.delete_table('moviedb_file')

        # Deleting model 'VideoTrack'
        db.delete_table('moviedb_videotrack')

        # Deleting model 'AudioTrack'
        db.delete_table('moviedb_audiotrack')

        # Deleting model 'SubtitleTrack'
        db.delete_table('moviedb_subtitletrack')

        # Deleting model 'Folder'
        db.delete_table('moviedb_folder')


    models = {
        'moviedb.actor': {
            'Meta': {'object_name': 'Actor'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'movie': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'actors'", 'to': "orm['moviedb.Movie']"}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['moviedb.Person']"}),
            'role': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['moviedb.Role']"})
        },
        'moviedb.audiotrack': {
            'Meta': {'object_name': 'AudioTrack'},
            'bitrate': ('django.db.models.fields.IntegerField', [], {}),
            'channels': ('django.db.models.fields.TextField', [], {'max_length': '5'}),
            'codec': ('django.db.models.fields.TextField', [], {'max_length': '20'}),
            'default': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'file': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'audioTracks'", 'to': "orm['moviedb.File']"}),
            'forced': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.TextField', [], {'max_length': '5'}),
            'name': ('django.db.models.fields.TextField', [], {'max_length': '30'}),
            'uid': ('django.db.models.fields.IntegerField', [], {})
        },
        'moviedb.country': {
            'Meta': {'object_name': 'Country'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {'unique': 'True', 'max_length': '30'})
        },
        'moviedb.file': {
            'Meta': {'object_name': 'File'},
            'duration': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'folder': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'files'", 'to': "orm['moviedb.Folder']"}),
            'format': ('django.db.models.fields.TextField', [], {'max_length': '20'}),
            'hash': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'movie': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'files'", 'null': 'True', 'to': "orm['moviedb.Movie']"}),
            'name': ('django.db.models.fields.TextField', [], {}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'childs'", 'null': 'True', 'to': "orm['moviedb.File']"}),
            'path': ('django.db.models.fields.TextField', [], {}),
            'size': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'type': ('django.db.models.fields.TextField', [], {'max_length': '20'})
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
            'name': ('django.db.models.fields.TextField', [], {'unique': 'True', 'max_length': '20'})
        },
        'moviedb.movie': {
            'Meta': {'object_name': 'Movie'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'cast': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['moviedb.Person']", 'through': "orm['moviedb.Actor']", 'symmetrical': 'False'}),
            'countries': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'movies'", 'symmetrical': 'False', 'to': "orm['moviedb.Country']"}),
            'directors': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'moviesDirector'", 'symmetrical': 'False', 'db_table': "'moviedb_movie_directors'", 'to': "orm['moviedb.Person']"}),
            'duration': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'genres': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'movies'", 'symmetrical': 'False', 'to': "orm['moviedb.Genre']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imdbID': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'languages': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'mdbID': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'resolution': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'writers': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'moviesWriter'", 'symmetrical': 'False', 'db_table': "'moviedb_movie_writers'", 'to': "orm['moviedb.Person']"}),
            'year': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'moviedb.person': {
            'Meta': {'object_name': 'Person'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imdbID': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'name': ('django.db.models.fields.TextField', [], {})
        },
        'moviedb.poster': {
            'Meta': {'object_name': 'Poster'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imageOriginal': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'imageThumb': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'movie': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'posters'", 'to': "orm['moviedb.Movie']"}),
            'name': ('django.db.models.fields.TextField', [], {'max_length': '200'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'remotePath': ('django.db.models.fields.TextField', [], {}),
            'sourceType': ('django.db.models.fields.TextField', [], {})
        },
        'moviedb.role': {
            'Meta': {'object_name': 'Role'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imdbID': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'name': ('django.db.models.fields.TextField', [], {'max_length': '30'})
        },
        'moviedb.subtitletrack': {
            'Meta': {'object_name': 'SubtitleTrack'},
            'codec': ('django.db.models.fields.TextField', [], {'max_length': '20'}),
            'default': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'file': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'subtitleTracks'", 'to': "orm['moviedb.File']"}),
            'forced': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.TextField', [], {'max_length': '5'}),
            'name': ('django.db.models.fields.TextField', [], {'max_length': '30'}),
            'uid': ('django.db.models.fields.IntegerField', [], {})
        },
        'moviedb.title': {
            'Meta': {'object_name': 'Title'},
            'comment': ('django.db.models.fields.TextField', [], {'max_length': '100', 'blank': 'True'}),
            'country': ('django.db.models.fields.TextField', [], {'max_length': '30', 'blank': 'True'}),
            'default': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.TextField', [], {'max_length': '30', 'blank': 'True'}),
            'movie': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'titles'", 'to': "orm['moviedb.Movie']"}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        'moviedb.videotrack': {
            'Meta': {'object_name': 'VideoTrack'},
            'bitrate': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'codec': ('django.db.models.fields.TextField', [], {'max_length': '20'}),
            'default': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'file': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'videoTracks'", 'to': "orm['moviedb.File']"}),
            'forced': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'height': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {'max_length': '30'}),
            'uid': ('django.db.models.fields.IntegerField', [], {}),
            'width': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['moviedb']
