# Generated by Django 4.2.7 on 2024-06-08 09:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='название')),
                ('image', models.ImageField(blank=True, null=True, upload_to='courses', verbose_name='превью')),
                ('description', models.TextField(blank=True, null=True, verbose_name='описание')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='дата и время создания')),
            ],
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='название')),
                ('description', models.TextField(blank=True, null=True, verbose_name='описание')),
                ('preview', models.ImageField(blank=True, null=True, upload_to='lesson', verbose_name='первью')),
                ('video_url', models.URLField(blank=True, null=True, verbose_name='видео')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='дата и время создания')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='education.course', verbose_name='курс')),
            ],
        ),
    ]
