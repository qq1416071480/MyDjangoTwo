# Generated by Django 3.2.7 on 2021-09-08 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apitest', '0003_alter_db_tucao_create_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='DB_home_href',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, null=True)),
                ('href', models.CharField(max_length=2000, null=True)),
            ],
        ),
    ]
