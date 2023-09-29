# Generated by Django 4.2 on 2023-09-29 01:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_userfollow'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='avatar_image',
            field=models.ImageField(default='image.png', upload_to='avatar/images/', verbose_name='avatar image'),
            preserve_default=False,
        ),
    ]