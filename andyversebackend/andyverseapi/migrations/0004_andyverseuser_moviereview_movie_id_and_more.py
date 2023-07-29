# Generated by Django 4.2.1 on 2023-07-02 17:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('andyverseapi', '0003_delete_futurereviews'),
    ]

    operations = [
        migrations.CreateModel(
            name='AndyVerseUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=150, unique=True)),
                ('email', models.CharField(max_length=50, unique=True)),
                ('uid', models.CharField(max_length=50, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('profile_img', models.URLField(default='')),
                ('is_staff', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['created'],
            },
        ),
        migrations.AddField(
            model_name='moviereview',
            name='movie_id',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='moviereview',
            name='favorited',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='moviereview',
            name='future',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='moviereview',
            name='poster_img',
            field=models.URLField(default=''),
        ),
        migrations.AlterField(
            model_name='moviereview',
            name='public',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='moviereview',
            name='spoiler_warning',
            field=models.BooleanField(default=True),
        ),
        migrations.DeleteModel(
            name='CustomUser',
        ),
        migrations.AlterField(
            model_name='moviereview',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='andyverseapi.andyverseuser'),
        ),
    ]
