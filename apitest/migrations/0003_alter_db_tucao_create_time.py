# Generated by Django 3.2.7 on 2021-09-08 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apitest', '0002_db_tucao'),
    ]

    operations = [
        migrations.AlterField(
            model_name='db_tucao',
            name='create_time',
            field=models.DateTimeField(auto_created=True),
        ),
    ]
