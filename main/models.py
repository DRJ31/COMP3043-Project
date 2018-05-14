# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Bulletin(models.Model):
    bid = models.AutoField(primary_key=True)
    uid = models.IntegerField(blank=True, null=True)
    time = models.DateTimeField(blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bulletin'


class Post(models.Model):
    pid = models.AutoField(primary_key=True)
    poster = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=1, blank=True, null=True)
    pic = models.TextField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    location = models.TextField(blank=True, null=True)
    locationrange = models.CharField(max_length=1, blank=True, null=True)
    contact = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'post'


class Readed(models.Model):
    uid = models.IntegerField(primary_key=True)
    status = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'readed'


class Userinfo(models.Model):
    username = models.TextField(blank=True, null=True)
    nickname = models.TextField(blank=True, null=True)
    email = models.TextField(blank=True, null=True)
    password = models.TextField(blank=True, null=True)
    role = models.CharField(max_length=5)
    activated = models.BooleanField()
    uid = models.AutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'userinfo'
