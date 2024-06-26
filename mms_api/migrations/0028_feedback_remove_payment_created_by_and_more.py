# Generated by Django 4.2.9 on 2024-04-03 18:13

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('mms_api', '0027_alter_payment_vendor_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='FeedBack',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('welcome', models.CharField(max_length=255)),
                ('welcome_notes', models.TextField()),
                ('service_level', models.CharField(max_length=255)),
                ('service_level_notes', models.TextField()),
                ('price_level', models.CharField(max_length=255)),
                ('price_level_notes', models.TextField()),
                ('food_level', models.CharField(max_length=255)),
                ('food_level_notes', models.TextField()),
                ('clean_level', models.CharField(max_length=255)),
                ('clean_level_notes', models.TextField()),
                ('client_name', models.CharField(max_length=255)),
                ('notes', models.TextField()),
                ('created_at', models.DateTimeField()),
            ],
        ),
        migrations.RemoveField(
            model_name='payment',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='vendor',
            name='account_manager',
        ),
        migrations.RemoveField(
            model_name='vendor',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='vendor',
            name='pay_period',
        ),
        migrations.RemoveField(
            model_name='vendor',
            name='pay_type',
        ),
        migrations.DeleteModel(
            name='PaidOrders',
        ),
        migrations.DeleteModel(
            name='Payment',
        ),
        migrations.DeleteModel(
            name='PaymentCycle',
        ),
        migrations.DeleteModel(
            name='PaymentMethod',
        ),
        migrations.DeleteModel(
            name='Vendor',
        ),
    ]
