# Generated by Django 4.1.5 on 2023-02-15 02:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('riaapp', '0004_alter_contact_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='Trainer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trainer_name', models.CharField(max_length=50)),
                ('trainer_designation', models.CharField(max_length=100)),
                ('trainer_experience', models.DecimalField(decimal_places=2, max_digits=5)),
                ('course', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='riaapp.cources')),
            ],
        ),
    ]
