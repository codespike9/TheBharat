# Generated by Django 4.2.3 on 2023-07-19 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0007_alter_news_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='cover_tags',
            field=models.CharField(default=None, max_length=255),
        ),
    ]
