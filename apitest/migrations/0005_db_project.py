# Generated by Django 3.2.7 on 2021-09-08 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apitest', '0004_db_home_href'),
    ]

    operations = [
        migrations.CreateModel(
            name='DB_project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, null=True)),
                ('remark', models.CharField(max_length=1000, null=True)),
                ('username', models.CharField(max_length=15, null=True)),
                ('other_user', models.CharField(max_length=100, null=True)),
            ],
        ),
    ]