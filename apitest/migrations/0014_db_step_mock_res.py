# Generated by Django 3.2.7 on 2021-10-09 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apitest', '0013_db_step'),
    ]

    operations = [
        migrations.AddField(
            model_name='db_step',
            name='mock_res',
            field=models.CharField(max_length=1000, null=True, verbose_name='mock返回值'),
        ),
    ]
