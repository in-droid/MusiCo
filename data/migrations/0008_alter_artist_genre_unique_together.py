# Generated by Django 4.0 on 2022-01-03 01:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0007_user_artist'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='artist_genre',
            unique_together={('aid', 'gid')},
        ),
    ]
