# Generated by Django 2.0.2 on 2018-02-22 21:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('slack_integration', '0004_auto_20180209_1749'),
    ]

    operations = [
        migrations.AlterField(
            model_name='slackuser',
            name='display_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
