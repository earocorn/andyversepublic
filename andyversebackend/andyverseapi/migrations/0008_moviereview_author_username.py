# Generated by Django 4.2.1 on 2023-07-13 20:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('andyverseapi', '0007_moviereview_review_summary'),
    ]

    operations = [
        migrations.AddField(
            model_name='moviereview',
            name='author_username',
            field=models.CharField(default='', max_length=50),
        ),
    ]
