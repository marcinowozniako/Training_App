# Generated by Django 4.0.4 on 2022-04-12 11:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('training', '0005_alter_trainingplan_reps_unit_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='workoutset',
            options={'ordering': ['exercise']},
        ),
        migrations.AddField(
            model_name='workoutset',
            name='date',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='workoutset',
            name='owner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
