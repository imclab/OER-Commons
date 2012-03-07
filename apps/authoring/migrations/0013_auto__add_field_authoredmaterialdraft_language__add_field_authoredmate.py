# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'AuthoredMaterialDraft.language'
        db.add_column('authoring_authoredmaterialdraft', 'language', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['materials.Language'], null=True), keep_default=False)

        # Adding field 'AuthoredMaterial.language'
        db.add_column('authoring_authoredmaterial', 'language', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['materials.Language'], null=True), keep_default=False)

        # Adding field 'AuthoredMaterial.slug'
        db.add_column('authoring_authoredmaterial', 'slug', self.gf('autoslug.fields.AutoSlugField')(default=u'', unique_with=(), max_length=50, populate_from=None, db_index=True), keep_default=False)

        # Adding field 'AuthoredMaterial.published_on'
        db.add_column('authoring_authoredmaterial', 'published_on', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True), keep_default=False)

        # Adding field 'AuthoredMaterial.featured'
        db.add_column('authoring_authoredmaterial', 'featured', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)

        # Adding field 'AuthoredMaterial.featured_on'
        db.add_column('authoring_authoredmaterial', 'featured_on', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'AuthoredMaterialDraft.language'
        db.delete_column('authoring_authoredmaterialdraft', 'language_id')

        # Deleting field 'AuthoredMaterial.language'
        db.delete_column('authoring_authoredmaterial', 'language_id')

        # Deleting field 'AuthoredMaterial.slug'
        db.delete_column('authoring_authoredmaterial', 'slug')

        # Deleting field 'AuthoredMaterial.published_on'
        db.delete_column('authoring_authoredmaterial', 'published_on')

        # Deleting field 'AuthoredMaterial.featured'
        db.delete_column('authoring_authoredmaterial', 'featured')

        # Deleting field 'AuthoredMaterial.featured_on'
        db.delete_column('authoring_authoredmaterial', 'featured_on')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
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
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'authoring.authoredmaterial': {
            'Meta': {'object_name': 'AuthoredMaterial'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['auth.User']"}),
            'created_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'featured': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'featured_on': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'grade_level': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.GradeLevel']", 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_new': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'keywords': ('core.fields.AutoCreateManyToManyField', [], {'to': "orm['materials.Keyword']", 'symmetrical': 'False'}),
            'language': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['materials.Language']", 'null': 'True'}),
            'learning_goals': ('core.fields.AutoCreateManyToManyField', [], {'to': "orm['authoring.LearningGoal']", 'symmetrical': 'False'}),
            'license': ('core.fields.AutoCreateForeignKey', [], {'to': "orm['materials.License']", 'null': 'True'}),
            'media_formats': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['common.MediaFormat']", 'symmetrical': 'False'}),
            'modified_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'owners': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'+'", 'symmetrical': 'False', 'to': "orm['auth.User']"}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'published_on': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique_with': '()', 'max_length': '50', 'populate_from': 'None', 'db_index': 'True'}),
            'subjects': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['materials.GeneralSubject']", 'symmetrical': 'False'}),
            'summary': ('django.db.models.fields.TextField', [], {'default': "u''"}),
            'text': ('django.db.models.fields.TextField', [], {'default': "u''"}),
            'title': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '200'})
        },
        'authoring.authoredmaterialdraft': {
            'Meta': {'object_name': 'AuthoredMaterialDraft'},
            'grade_level': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.GradeLevel']", 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keywords': ('core.fields.AutoCreateManyToManyField', [], {'to': "orm['materials.Keyword']", 'symmetrical': 'False'}),
            'language': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['materials.Language']", 'null': 'True'}),
            'learning_goals': ('core.fields.AutoCreateManyToManyField', [], {'to': "orm['authoring.LearningGoal']", 'symmetrical': 'False'}),
            'license': ('core.fields.AutoCreateForeignKey', [], {'to': "orm['materials.License']", 'null': 'True'}),
            'material': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'draft'", 'unique': 'True', 'to': "orm['authoring.AuthoredMaterial']"}),
            'subjects': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['materials.GeneralSubject']", 'symmetrical': 'False'}),
            'summary': ('django.db.models.fields.TextField', [], {'default': "u''"}),
            'text': ('django.db.models.fields.TextField', [], {'default': "u''"}),
            'title': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '200'})
        },
        'authoring.document': {
            'Meta': {'object_name': 'Document'},
            'file': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'material': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['authoring.AuthoredMaterial']"})
        },
        'authoring.embed': {
            'Meta': {'object_name': 'Embed'},
            'embed_url': ('django.db.models.fields.URLField', [], {'db_index': 'True', 'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'html': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'thumbnail': ('django.db.models.fields.URLField', [], {'db_index': 'True', 'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '20', 'db_index': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'unique': 'True', 'max_length': '200', 'db_index': 'True'})
        },
        'authoring.image': {
            'Meta': {'object_name': 'Image'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'material': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['authoring.AuthoredMaterial']"})
        },
        'authoring.learninggoal': {
            'Meta': {'object_name': 'LearningGoal'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'common.gradelevel': {
            'Meta': {'ordering': "('id',)", 'object_name': 'GradeLevel'},
            'description': ('django.db.models.fields.TextField', [], {'default': "u''", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique': 'True', 'max_length': '100', 'populate_from': 'None', 'unique_with': '()', 'db_index': 'True'})
        },
        'common.mediaformat': {
            'Meta': {'ordering': "('id',)", 'object_name': 'MediaFormat'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique': 'True', 'max_length': '100', 'populate_from': 'None', 'unique_with': '()', 'db_index': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'materials.generalsubject': {
            'Meta': {'ordering': "('id',)", 'object_name': 'GeneralSubject'},
            'description': ('django.db.models.fields.TextField', [], {'default': "u''", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique': 'True', 'max_length': '100', 'populate_from': 'None', 'unique_with': '()', 'db_index': 'True'})
        },
        'materials.keyword': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Keyword'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '500'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique_with': '()', 'max_length': '500', 'populate_from': 'None', 'db_index': 'True'}),
            'suggested': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'materials.language': {
            'Meta': {'ordering': "('order', 'name')", 'object_name': 'Language'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '999'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '3', 'db_index': 'True'})
        },
        'materials.license': {
            'Meta': {'ordering': "('id',)", 'object_name': 'License'},
            'copyright_holder': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '2000', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'default': "u''", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_url': ('django.db.models.fields.URLField', [], {'default': "u''", 'max_length': '300', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '300'}),
            'url': ('django.db.models.fields.URLField', [], {'default': "u''", 'max_length': '300', 'blank': 'True'})
        }
    }

    complete_apps = ['authoring']
