# Generated by Django 4.0.4 on 2022-04-11 14:29

from django.db import migrations
import embed_video.fields


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0002_alter_exercises_options_alter_training_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='exercises',
            name='video',
            field=embed_video.fields.EmbedVideoField(blank=True, null=True),
        ),
    ]
