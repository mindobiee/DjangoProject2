# Generated by Django 3.1.2 on 2020-11-04 08:06

from django.db import migrations
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0003_taggeditem_add_unique_index'),
        ('photo', '0003_auto_20201104_1701'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='tags',
            field=taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]
