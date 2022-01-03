# Generated by Django 4.0 on 2022-01-03 01:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('data', '0006_alter_artist_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='User_Artist',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('artist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data.artist')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.user')),
            ],
            options={
                'unique_together': {('user', 'artist')},
            },
        ),
    ]
