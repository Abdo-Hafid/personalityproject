# Generated by Django 4.2.7 on 2024-05-09 21:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TestPersonality', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidat',
            name='age_range',
            field=models.CharField(choices=[('20-30', '20-30'), ('30-40', '40-40'), ('40-50', '40-50'), ('>50', '>50')], max_length=10, null=True),
        ),
    ]
