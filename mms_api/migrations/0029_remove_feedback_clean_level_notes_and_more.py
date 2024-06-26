# Generated by Django 4.2.9 on 2024-04-03 19:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mms_api', '0028_feedback_remove_payment_created_by_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='feedback',
            name='clean_level_notes',
        ),
        migrations.RemoveField(
            model_name='feedback',
            name='food_level_notes',
        ),
        migrations.RemoveField(
            model_name='feedback',
            name='price_level_notes',
        ),
        migrations.RemoveField(
            model_name='feedback',
            name='service_level_notes',
        ),
        migrations.RemoveField(
            model_name='feedback',
            name='welcome_notes',
        ),
        migrations.AlterField(
            model_name='feedback',
            name='created_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='feedback',
            name='notes',
            field=models.TextField(blank=True),
        ),
    ]
