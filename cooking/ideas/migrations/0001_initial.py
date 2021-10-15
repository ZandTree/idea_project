# Generated by Django 3.2.4 on 2021-08-24 11:52

import autoslug.fields
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import timestamp.broadcast_utils.idea_utils
import timestamp.broadcast_utils.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, unique=True)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from='name', unique=True)),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('mptt_level', models.PositiveIntegerField(editable=False)),
            ],
            options={
                'verbose_name_plural': 'Categories',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Idea',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=240)),
                ('slug', models.SlugField(blank=True, max_length=255, unique=True)),
                ('lead_text', models.CharField(default='', max_length=254)),
                ('main_text', models.TextField()),
                ('view_count', models.IntegerField(blank=True, default=0)),
                ('thumbnail', models.ImageField(blank=True, null=True, upload_to=timestamp.broadcast_utils.idea_utils.upload_img, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=('JPG', 'JPEG', 'PNG')), timestamp.broadcast_utils.validators.validate_size])),
                ('featured', models.BooleanField(blank=True, default=False)),
                ('is_public', models.BooleanField(default=True)),
                ('status', models.IntegerField(choices=[(0, 'in progres'), (1, 'in review'), (3, 'published')], default=0)),
                ('avg_rate', models.DecimalField(decimal_places=2, default=None, max_digits=5, null=True)),
                ('an_likes', models.IntegerField(default=None, null=True)),
                ('max_rating', models.DecimalField(decimal_places=2, default=None, max_digits=5, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UserIdeaRelation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('like', models.BooleanField(blank=True, default=False)),
                ('dislike', models.BooleanField(blank=True, default=False)),
                ('in_bookmark', models.BooleanField(blank=True, default=False)),
                ('rating', models.PositiveSmallIntegerField(blank=True, choices=[(1, 'OK'), (2, 'Fine'), (3, 'Good'), (4, 'Amazing'), (5, 'Excellent')], null=True)),
                ('idea', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ideas.idea')),
            ],
        ),
    ]
