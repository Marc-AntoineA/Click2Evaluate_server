# Generated by Django 2.0 on 2017-12-29 21:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answered', models.BooleanField(default=False)),
                ('typeform', models.CharField(max_length=50)),
                ('answer', models.CharField(max_length=20000)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_course', models.CharField(max_length=10)),
                ('label', models.CharField(max_length=100)),
                ('delegates', models.CharField(max_length=1000)),
                ('commissionsDate', models.DateTimeField()),
                ('availableDate', models.DateTimeField()),
                ('typeform', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ldap', models.CharField(max_length=100)),
                ('course', models.ManyToManyField(to='main.Course')),
            ],
        ),
        migrations.AddField(
            model_name='answer',
            name='course',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='main.Course'),
        ),
        migrations.AddField(
            model_name='answer',
            name='student',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='main.Student'),
        ),
    ]
