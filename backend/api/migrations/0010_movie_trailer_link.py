# Generated by Django 5.0.2 on 2024-03-08 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_alter_comment_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='trailer_link',
            field=models.CharField(blank=True, max_length=1000000, null=True, verbose_name='Movie Trailer Link'),
        ),
    ]