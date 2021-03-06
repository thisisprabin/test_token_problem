# Generated by Django 3.1.3 on 2020-11-08 12:38

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Token',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('token', models.CharField(max_length=320)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('expire_time', models.DateTimeField(blank=True, default=None, null=True)),
                ('last_used', models.DateTimeField(blank=True, default=None, null=True)),
                ('is_assigned', models.BooleanField(default=False)),
                ('deleted', models.BooleanField(default=False)),
            ],
        ),
    ]
