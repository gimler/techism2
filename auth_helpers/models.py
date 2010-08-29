"""
Models for object-level permissions
"""

from django.db import models
from django.contrib.auth.models import User, Group
from django.contrib.contenttypes.models import ContentType

from djangotoolbox.fields import ListField

class ObjectPermission(models.Model):
    user = models.ForeignKey(User, null=True)

    permission_list = ListField(models.CharField(max_length=64))
                            
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()


class GroupObjectPermission(models.Model):
    group = models.ForeignKey(Group, null=True)

    permission_list = ListField(models.CharField(max_length=64))
                            
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()


class PermissionType(models.Model):
    content_type = models.ForeignKey(ContentType, null=True)
    permission_name = models.CharField(max_length=64, null=True)
