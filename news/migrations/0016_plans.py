# Generated by Django 4.2.3 on 2023-07-31 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0015_news_editorial_pick'),
    ]

    operations = [
        migrations.CreateModel(
            name='Plans',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plan', models.CharField(max_length=255)),
                ('price', models.FloatField()),
                ('extra_features', models.BooleanField(default=True)),
                ('soft_copy', models.BooleanField(default=True)),
                ('weekly_magazine', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name_plural': 'Plans',
            },
        ),
    ]
