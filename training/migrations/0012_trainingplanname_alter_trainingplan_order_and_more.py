# Generated by Django 4.0.4 on 2022-04-16 22:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0011_alter_training_options_alter_trainingplan_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='TrainingPlanName',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('training_plan_name', models.CharField(max_length=256)),
            ],
        ),
        migrations.AlterField(
            model_name='trainingplan',
            name='order',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='workoutset',
            name='date',
            field=models.DateField(blank=True, default='2022-04-17', null=True),
        ),
        migrations.AlterField(
            model_name='workoutset',
            name='day',
            field=models.ForeignKey(default=7, on_delete=django.db.models.deletion.CASCADE, to='training.dayname'),
        ),
        migrations.AddField(
            model_name='trainingplan',
            name='training_plan_nb',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='training.trainingplanname'),
        ),
    ]
