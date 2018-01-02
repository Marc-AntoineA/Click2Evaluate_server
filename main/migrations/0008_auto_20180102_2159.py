# Generated by Django 2.0 on 2018-01-02 21:59

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_auto_20180102_2117'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuestionWithAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answered', models.BooleanField(default=False)),
                ('submissionDate', models.DateTimeField(blank=True, default=django.utils.timezone.now)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Group')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Student')),
            ],
        ),
        migrations.RemoveField(
            model_name='answer',
            name='group',
        ),
        migrations.RemoveField(
            model_name='answer',
            name='student',
        ),
        migrations.RenameField(
            model_name='question',
            old_name='resume',
            new_name='summary',
        ),
        migrations.RenameField(
            model_name='question',
            old_name='survey',
            new_name='typeForm',
        ),
        migrations.AlterField(
            model_name='course',
            name='id_course',
            field=models.CharField(max_length=10, unique=True),
        ),
        migrations.AlterField(
            model_name='course',
            name='label',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='typeform',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.DeleteModel(
            name='Answer',
        ),
        migrations.AddField(
            model_name='questionwithanswer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Question'),
        ),
        migrations.AddField(
            model_name='questionwithanswer',
            name='survey',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Survey'),
        ),
    ]
