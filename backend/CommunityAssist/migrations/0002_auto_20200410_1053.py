# Generated by Django 2.1 on 2020-04-10 10:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CommunityAssist', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userbigtable',
            name='availableQuanity',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='userbigtable',
            name='categoryType',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='userbigtable',
            name='column1',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='userbigtable',
            name='column2',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='userbigtable',
            name='column3',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='userbigtable',
            name='column4',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='userbigtable',
            name='column5',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='userbigtable',
            name='dateAvailable',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='userbigtable',
            name='description',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='userbigtable',
            name='productName',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='userbigtable',
            name='timeAvailable',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='userbigtable',
            name='actionType',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='userbigtable',
            name='address',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='userbigtable',
            name='dateCreated',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='userbigtable',
            name='firstname',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='userbigtable',
            name='lastname',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='userbigtable',
            name='password',
            field=models.CharField(max_length=200, null=True),
        ),
    ]