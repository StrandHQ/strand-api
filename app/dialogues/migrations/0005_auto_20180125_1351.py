# Generated by Django 2.0.1 on 2018-01-25 13:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dialogues', '0004_auto_20180123_1636'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='message',
            name='origin_slack_event',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='message', to='slack_integration.SlackEvent'),
        ),
        migrations.AlterField(
            model_name='message',
            name='discussion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='topics.Discussion'),
        ),
        migrations.AlterField(
            model_name='reply',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='replies', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='reply',
            name='message',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='dialogues.Message'),
        ),
        migrations.AlterField(
            model_name='reply',
            name='origin_slack_event',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reply', to='slack_integration.SlackEvent'),
        ),
    ]
