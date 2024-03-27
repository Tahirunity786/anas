# Generated by Django 5.0.3 on 2024-03-21 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EngineDB',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Image', models.ImageField(db_index=True, upload_to='temp/dicom')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
