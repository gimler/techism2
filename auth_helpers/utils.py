from django.contrib.auth.models import User
from django.db import models
from django.contrib.contenttypes.models import ContentType

from models import ObjectPermission, PermissionType, GroupObjectPermission

def register(model_class, perm):
    """
    creates a PermissionType object with permission perm for the model model_class
    """

    ct = ContentType.objects.get_for_model(model_class)
    pt = PermissionType.objects.filter(content_type=ct,
                                       permission_name=perm)

    if pt.count() != 0:
        return False # already registered
    else:
        pt = PermissionType(content_type=ct, permission_name=perm)
        pt.save()
        return True
    
def grant_permissions(model, user, permission_list):
    """
    add permission_list for user to model

    returns False if permission_list contains unregistered permissions
    or model is no instance of models.Model or user is no instance of
    django.contrib.auth.models.User

    returns True if permission_list is saved
    """
    
    if isinstance(user, User) and isinstance(model, models.Model):
        ct = ContentType.objects.get_for_model(model)
        try:
            perm_obj = ObjectPermission.objects.get(user=user,
                                                    content_type=ct,
                                                   object_id=model.id)

        except ObjectPermission.DoesNotExist:
            perm_obj = ObjectPermission(user=user, 
                                         content_type=ct, object_id=model.id)
        current_permission_list = perm_obj.permission_list
        registered_permissions = PermissionType.objects.filter(content_type=
                                                               ct)

        registerd_permission_list = list()
        
        for perm in registered_permissions:
            registerd_permission_list.append(perm.permission_name)
        
        
        # remove already existing entries from permission_list
        for perm in current_permission_list:
            try:
                dup = permission_list.index(perm)
                permission_list.remove(dup)
            except ValueError:
                pass
            
        for perm in permission_list:
            try:
                perm_obj.permission_list.append(registerd_permission_list.pop(registerd_permission_list.index(perm)))
            except ValueError:
                return False
            
        perm_obj.save()
        return True

    else:
        return False


def add_permission_to_group(perm, group, obj):
    ct = ContentType.objects.get_for_model(obj)
    perm_obj, created = GroupObjectPermission.objects.get_or_create(group=group,
                                                                    content_type=ct,
                                                                    object_id=obj.id)
        
    

    perm_obj.permission_list.append(perm)

    perm_obj.save()
    

