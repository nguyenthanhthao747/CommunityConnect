# Generated by Django 2.1 on 2020-04-10 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CommunityAssist', '0002_auto_20200410_1053'),
    ]

    operations = [
        migrations.AddField(
            model_name='userbigtable',
            name='column6',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='userbigtable',
            name='column7',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='userbigtable',
            name='column8',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='userbigtable',
            name='phoneNumber',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='userbigtable',
            name='state',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='userbigtable',
            name='subCategoryType',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='userbigtable',
            name='suburb',
            field=models.CharField(max_length=200, null=True),
        ),
    ]