# Generated by Django 4.0.4 on 2022-04-12 14:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0007_training_owner_trainingplan_owner'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='training',
            options={'ordering': ['owner']},
        ),
    ]
