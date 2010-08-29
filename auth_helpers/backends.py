from django.conf import settings
from django.contrib.contenttypes.models import ContentType

from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend

from google.appengine.api import users

from djangotoolbox.auth.models import GroupList

from models import ObjectPermission, GroupObjectPermission


class GoogleAccountBackend(ModelBackend):
    """
    backend for authentication via Google Accounts on Google
    App Engine

    A Django auth.contrib.models.User object is linked to
    a Google Account via the password field, that stores
    the unique Google Account ID
    The Django User object is created the first time a user logs
    in with his Google Account.
    """

    def authenticate(self):
        g_user = users.get_current_user()

        if g_user == None:
            return None

        username = g_user.email().split('@')[0]

        if hasattr(settings, 'ALLOWED_USERS'):
            try:
                settings.ALLOWED_USERS.index(username)
            except ValueError:
                return None
            
        try:
            user = User.objects.get(password=g_user.user_id())
            if user.email is not g_user.email():
                user.email = g_user.email()
                user.username = username
                user.save()
 
            return user
        except User.DoesNotExist:
                user = User.objects.create_user(username,\
                                                g_user.email())
                user.password = g_user.user_id()
                if users.is_current_user_admin():
                    user.is_staff = True
                    user.is_superuser = True
                user.save()
                return user


class ObjectPermBackend(object):
    supports_object_permissions = True
    supports_anonymous_user = True
    
    def authenticate(self, username, password):
        return None

    def has_perm(self, user_obj, perm, obj=None):
        return perm in self.get_all_permissions(user_obj, obj)
    
    def get_all_permissions(self, user_obj, obj=None):
        if not user_obj.is_authenticated():
            try:
                user_obj = User.objects.get(pk=settings.ANONYMOUS_USER_ID)
            except User.DoesNotExist:
                user_obj = User(username='AnonymousUser', email='ano@nymous.xfz')
                user_obj.set_unusable_password()
                
        if obj is None:
            return set()
                
        ct = ContentType.objects.get_for_model(obj)
        
        current_permission_objs = ObjectPermission.objects.filter(content_type=ct,
                                                                  object_id=obj.id,
                                                                  user=user_obj)
        perms = set()
        
        for p in current_permission_objs:
            perms.update(p.permission_list)

        perms.update(self.get_group_permissions(user_obj, obj))
        return perms
            
    def get_group_permissions(self, user_obj, obj=None):
        if obj is None:
            return set()

        if not user_obj.is_authenticated():
            return set()


        ct = ContentType.objects.get_for_model(obj)

        try:
            group_list = GroupList.objects.get(user=user_obj)
            
            current_permission_objs = GroupObjectPermission.objects.filter(content_type=ct,
                                                                           object_id=obj.id,
                                                                           group__in=group_list.groups)
            perms = set()
            for p in current_permission_objs:
                perms.update(p.permission_list)

            return perms
        except GroupList.DoesNotExist:
            return set()
