# Generated by Django 3.0.6 on 2020-07-20 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0002_auto_20200720_2152'),
    ]

    operations = [
        migrations.CreateModel(
            name='CamsLogInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chaturbate_username', models.CharField(blank=True, max_length=64)),
                ('status', models.CharField(blank=True, default='Online', max_length=20)),
            ],
        ),
    ]
