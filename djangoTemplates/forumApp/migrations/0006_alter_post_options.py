# Generated by Django 5.1.1 on 2024-11-02 08:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forumApp', '0005_post_approved'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'permissions': [('can_approve_posts', 'Can approve posts')]},
        ),
    ]