# Generated by Django 2.0.1 on 2018-01-04 20:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20180103_1405'),
    ]

    operations = [
        migrations.RenameField(
            model_name='question',
            old_name='parentsquestionsValue',
            new_name='parentsQuestionsValue',
        ),
    ]