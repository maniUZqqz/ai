# Generated by Django 5.0.7 on 2024-11-24 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ai', '0003_conversation_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='conversation',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]
