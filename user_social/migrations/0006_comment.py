# Generated by Django 4.0.2 on 2022-04-13 18:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_social', '0005_post'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=150)),
                ('at', models.DateTimeField(auto_now_add=True)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_social.post')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_social.user')),
            ],
        ),
    ]
