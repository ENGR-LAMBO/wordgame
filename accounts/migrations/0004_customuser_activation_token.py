# Generated by Django 5.0.6 on 2024-06-17 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_customuser_email_verification_token_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='activation_token',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
    ]
