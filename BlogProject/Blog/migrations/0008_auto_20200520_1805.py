# Generated by Django 3.0.5 on 2020-05-20 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Blog', '0007_auto_20200520_1527'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='post_caption',
            field=models.CharField(max_length=100, verbose_name='Caption for your post'),
        ),
        migrations.AlterField(
            model_name='post',
            name='post_text',
            field=models.TextField(blank=True, null=True, verbose_name='Write your post here'),
        ),
    ]
