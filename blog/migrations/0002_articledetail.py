# Generated by Django 3.2.7 on 2022-04-09 06:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleDetail',
            fields=[
                ('nid', models.AutoField(primary_key=True, serialize=False)),
                ('content', models.TextField()),
                ('article', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='blog.article')),
            ],
            options={
                'verbose_name': '文章详情',
                'verbose_name_plural': '文章详情',
            },
        ),
    ]
