# Generated by Django 3.2 on 2021-05-27 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='name',
            field=models.CharField(choices=[('Expense', 'Expense'), ('Income', 'Income'), ('Savings', 'Savings')], max_length=7, unique=True),
        ),
    ]