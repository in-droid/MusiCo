# Generated by Django 4.0 on 2022-01-02 13:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('data', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User_Genre',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('gid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data.genre')),
                ('uid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.user')),
            ],
        ),
    ]
