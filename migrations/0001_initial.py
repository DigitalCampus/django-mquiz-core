# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Question'
        db.create_table('mquiz_question', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('created_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('lastupdated_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('title', self.gf('django.db.models.fields.TextField')()),
            ('type', self.gf('django.db.models.fields.CharField')(default='multichoice', max_length=15)),
        ))
        db.send_create_signal('mquiz', ['Question'])

        # Adding model 'Response'
        db.create_table('mquiz_response', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mquiz.Question'])),
            ('created_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('lastupdated_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('score', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=6, decimal_places=2)),
            ('title', self.gf('django.db.models.fields.TextField')()),
            ('order', self.gf('django.db.models.fields.IntegerField')(default=1)),
        ))
        db.send_create_signal('mquiz', ['Response'])

        # Adding model 'Quiz'
        db.create_table('mquiz_quiz', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('created_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('lastupdated_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('draft', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('title', self.gf('django.db.models.fields.TextField')()),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('mquiz', ['Quiz'])

        # Adding model 'QuizQuestion'
        db.create_table('mquiz_quizquestion', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('quiz', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mquiz.Quiz'])),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mquiz.Question'])),
            ('order', self.gf('django.db.models.fields.IntegerField')(default=1)),
        ))
        db.send_create_signal('mquiz', ['QuizQuestion'])

        # Adding model 'QuizProps'
        db.create_table('mquiz_quizprops', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('quiz', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mquiz.Quiz'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('value', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('mquiz', ['QuizProps'])

        # Adding model 'QuestionProps'
        db.create_table('mquiz_questionprops', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mquiz.Question'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('value', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('mquiz', ['QuestionProps'])

        # Adding model 'ResponseProps'
        db.create_table('mquiz_responseprops', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('response', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mquiz.Response'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('value', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('mquiz', ['ResponseProps'])

        # Adding model 'QuizAttempt'
        db.create_table('mquiz_quizattempt', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('quiz', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mquiz.Quiz'])),
            ('attempt_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('submitted_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('score', self.gf('django.db.models.fields.DecimalField')(max_digits=6, decimal_places=2)),
            ('maxscore', self.gf('django.db.models.fields.DecimalField')(max_digits=6, decimal_places=2)),
            ('ip', self.gf('django.db.models.fields.IPAddressField')(max_length=15)),
            ('agent', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('mquiz', ['QuizAttempt'])

        # Adding model 'QuizAttemptResponse'
        db.create_table('mquiz_quizattemptresponse', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('quizattempt', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mquiz.QuizAttempt'])),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mquiz.Question'])),
            ('score', self.gf('django.db.models.fields.DecimalField')(max_digits=6, decimal_places=2)),
            ('text', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('mquiz', ['QuizAttemptResponse'])


    def backwards(self, orm):
        # Deleting model 'Question'
        db.delete_table('mquiz_question')

        # Deleting model 'Response'
        db.delete_table('mquiz_response')

        # Deleting model 'Quiz'
        db.delete_table('mquiz_quiz')

        # Deleting model 'QuizQuestion'
        db.delete_table('mquiz_quizquestion')

        # Deleting model 'QuizProps'
        db.delete_table('mquiz_quizprops')

        # Deleting model 'QuestionProps'
        db.delete_table('mquiz_questionprops')

        # Deleting model 'ResponseProps'
        db.delete_table('mquiz_responseprops')

        # Deleting model 'QuizAttempt'
        db.delete_table('mquiz_quizattempt')

        # Deleting model 'QuizAttemptResponse'
        db.delete_table('mquiz_quizattemptresponse')


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
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'mquiz.question': {
            'Meta': {'object_name': 'Question'},
            'created_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastupdated_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'title': ('django.db.models.fields.TextField', [], {}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'multichoice'", 'max_length': '15'})
        },
        'mquiz.questionprops': {
            'Meta': {'object_name': 'QuestionProps'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mquiz.Question']"}),
            'value': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        'mquiz.quiz': {
            'Meta': {'object_name': 'Quiz'},
            'created_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'draft': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastupdated_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'questions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['mquiz.Question']", 'through': "orm['mquiz.QuizQuestion']", 'symmetrical': 'False'}),
            'title': ('django.db.models.fields.TextField', [], {})
        },
        'mquiz.quizattempt': {
            'Meta': {'object_name': 'QuizAttempt'},
            'agent': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'attempt_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'maxscore': ('django.db.models.fields.DecimalField', [], {'max_digits': '6', 'decimal_places': '2'}),
            'quiz': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mquiz.Quiz']"}),
            'score': ('django.db.models.fields.DecimalField', [], {'max_digits': '6', 'decimal_places': '2'}),
            'submitted_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'mquiz.quizattemptresponse': {
            'Meta': {'object_name': 'QuizAttemptResponse'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mquiz.Question']"}),
            'quizattempt': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mquiz.QuizAttempt']"}),
            'score': ('django.db.models.fields.DecimalField', [], {'max_digits': '6', 'decimal_places': '2'}),
            'text': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        'mquiz.quizprops': {
            'Meta': {'object_name': 'QuizProps'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'quiz': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mquiz.Quiz']"}),
            'value': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        'mquiz.quizquestion': {
            'Meta': {'object_name': 'QuizQuestion'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mquiz.Question']"}),
            'quiz': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mquiz.Quiz']"})
        },
        'mquiz.response': {
            'Meta': {'object_name': 'Response'},
            'created_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastupdated_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mquiz.Question']"}),
            'score': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '6', 'decimal_places': '2'}),
            'title': ('django.db.models.fields.TextField', [], {})
        },
        'mquiz.responseprops': {
            'Meta': {'object_name': 'ResponseProps'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'response': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mquiz.Response']"}),
            'value': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        }
    }

    complete_apps = ['mquiz']