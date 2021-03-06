# Generated by Django 2.0.1 on 2018-02-04 23:38

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_course', models.CharField(max_length=10, unique=True)),
                ('label', models.CharField(max_length=100)),
                ('commissionsDate', models.DateTimeField()),
                ('availableDate', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Departement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(default=0)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Course')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.IntegerField()),
                ('title', models.CharField(max_length=100)),
                ('label', models.CharField(max_length=300)),
                ('obligatory', models.BooleanField(default=False)),
                ('type_question', models.CharField(max_length=50, validators=[django.core.validators.RegexValidator(message='Veuillez choisir un type de question parmi select, selectOne, inline ou text', regex='^(select|selectOne|inline|text|number)$')])),
                ('type_data', models.CharField(blank=True, max_length=400)),
                ('isSub', models.BooleanField(max_length=50)),
                ('parentsQuestionPosition', models.IntegerField(default=0)),
                ('parentsQuestionsValue', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='QuestionWithAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.CharField(blank=True, default='', max_length=400)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Question')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ldap', models.CharField(max_length=100, unique=True)),
                ('first_name', models.CharField(max_length=20)),
                ('last_name', models.CharField(max_length=20)),
                ('mail', models.CharField(max_length=100, unique=True)),
                ('departement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Departement')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answered', models.BooleanField(default=False)),
                ('submissionDate', models.DateTimeField(blank=True, default=django.utils.timezone.now)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Group')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Student')),
            ],
        ),
        migrations.CreateModel(
            name='TypeForm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField(blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='questionwithanswer',
            name='survey',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Survey'),
        ),
        migrations.AddField(
            model_name='question',
            name='typeForm',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.TypeForm'),
        ),
        migrations.AddField(
            model_name='group',
            name='delegate',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Student'),
        ),
        migrations.AddField(
            model_name='course',
            name='typeForm',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.TypeForm'),
        ),
    ]
