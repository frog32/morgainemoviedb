# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting model 'Role'
        db.delete_table('moviedb_role')

        # Deleting model 'Actor'
        db.delete_table('moviedb_actor')

        # Adding model 'Job'
        db.create_table('moviedb_job', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('character', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('department', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['moviedb.Person'])),
            ('movie', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['moviedb.Movie'])),
        ))
        db.send_create_signal('moviedb', ['Job'])

        # Adding field 'Genre.tmdb_id'
        db.add_column('moviedb_genre', 'tmdb_id', self.gf('django.db.models.fields.IntegerField')(default=0), keep_default=False)

        # Deleting field 'Person.imdb_id'
        db.delete_column('moviedb_person', 'imdb_id')

        # Adding field 'Person.tmdb_id'
        db.add_column('moviedb_person', 'tmdb_id', self.gf('django.db.models.fields.IntegerField')(default=0), keep_default=False)

        # Removing M2M table for field writers on 'Movie'
        db.delete_table('moviedb_movie_writers')

        # Removing M2M table for field directors on 'Movie'
        db.delete_table('moviedb_movie_directors')

        # Adding field 'Country.code'
        db.add_column('moviedb_country', 'code', self.gf('django.db.models.fields.CharField')(default='', unique=True, max_length=10), keep_default=False)

        # Removing unique constraint on 'Country', fields ['name']
        db.delete_unique('moviedb_country', ['name'])


    def backwards(self, orm):
        
        # Adding model 'Role'
        db.create_table('moviedb_role', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('imdb_id', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('moviedb', ['Role'])

        # Adding model 'Actor'
        db.create_table('moviedb_actor', (
            ('movie', self.gf('django.db.models.fields.related.ForeignKey')(related_name='actors', to=orm['moviedb.Movie'])),
            ('role', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['moviedb.Role'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['moviedb.Person'])),
        ))
        db.send_create_signal('moviedb', ['Actor'])

        # Deleting model 'Job'
        db.delete_table('moviedb_job')

        # Deleting field 'Genre.tmdb_id'
        db.delete_column('moviedb_genre', 'tmdb_id')

        # Adding field 'Person.imdb_id'
        db.add_column('moviedb_person', 'imdb_id', self.gf('django.db.models.fields.IntegerField')(default=0), keep_default=False)

        # Deleting field 'Person.tmdb_id'
        db.delete_column('moviedb_person', 'tmdb_id')

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

        # Deleting field 'Country.code'
        db.delete_column('moviedb_country', 'code')

        # Adding unique constraint on 'Country', fields ['name']
        db.create_unique('moviedb_country', ['name'])


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
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
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
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'}),
            'tmdb_id': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'moviedb.job': {
            'Meta': {'object_name': 'Job'},
            'character': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'department': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'movie': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['moviedb.Movie']"}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['moviedb.Person']"})
        },
        'moviedb.movie': {
            'Meta': {'object_name': 'Movie'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'bookmarkedMovies': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'bookmarkedUsers'", 'blank': 'True', 'through': "orm['moviedb.Bookmark']", 'to': "orm['auth.User']"}),
            'countries': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'movies'", 'blank': 'True', 'to': "orm['moviedb.Country']"}),
            'duration': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'genres': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'movies'", 'blank': 'True', 'to': "orm['moviedb.Genre']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imdb_id': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'languages': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'resolution': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'tmdb_id': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'year': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'moviedb.person': {
            'Meta': {'object_name': 'Person'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'tmdb_id': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'moviedb.poster': {
            'Meta': {'object_name': 'Poster'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_original': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'image_thumb': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'movie': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'posters'", 'to': "orm['moviedb.Movie']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'remote_path': ('django.db.models.fields.TextField', [], {}),
            'source_type': ('django.db.models.fields.TextField', [], {})
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
            'file': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'video_tracks'", 'to': "orm['moviedb.File']"}),
            'forced': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'height': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'uid': ('django.db.models.fields.IntegerField', [], {}),
            'width': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['moviedb']
