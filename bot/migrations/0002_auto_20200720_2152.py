# Generated by Django 3.0.6 on 2020-07-20 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofileinfo',
            name='portfolio_site',
        ),
        migrations.AddField(
            model_name='userprofileinfo',
            name='chaturbate_password',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='userprofileinfo',
            name='chaturbate_username',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
    ]
