from django.db import models

# Create your models here.
class UserBigTable(models.Model):
    email = models.CharField(max_length=200)
    firstname = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    actionType = models.CharField(max_length=200)
    dateCreated = models.DateTimeField('date published')
