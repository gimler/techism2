from django.test import TestCase
from django.db import models
from django.contrib.auth.models import User, Group
from django.contrib.contenttypes.models import ContentType

from djangotoolbox.auth.utils import add_user_to_group

from .models import ObjectPermission,PermissionType, GroupObjectPermission
from .utils import grant_permissions, register, add_permission_to_group

class TestObj(models.Model):
    pass

class ObjPermBackendTests(TestCase):
    """
    Tests for the object permission app
    """

    def setUp(self):
        self.user1 = User.objects.create_user('test1', 'test1@test.com', 'test')
        self.user2 = User.objects.create_user('test2', 'test2@test.com', 'test')

        self.obj1 = TestObj()
        self.obj1.id = 1 # add id manually to avoid problem with app engine
        self.obj1.save()

    def test_permission_creation(self):
        ct = ContentType.objects.get_for_model(self.obj1)
        # add permission types
        pt = PermissionType(content_type=ct, permission_name='view')
        pt.save()
        pt = PermissionType(content_type=ct, permission_name='change')
        pt.save()
        pt = PermissionType(content_type=ct, permission_name='delete')
        pt.save()
        
        # create permission object for user1
        
        perm_obj = ObjectPermission.objects.create(user=self.user1,
                                                   content_type=ct, object_id=self.obj1.id)
        perm_obj.permission_list.append('view')
        perm_obj.permission_list.append('change')
        perm_obj.permission_list.append('delete')
        
        perm_obj.save()

        # a ObjectPermission object has to be created
        self.assertEquals(ObjectPermission.objects.count(), 1)
        
        # check if user1 has view, change and delete permission
        self.assertEquals(self.user1.has_perm('view', self.obj1), True)
        self.assertEquals(self.user1.has_perm('change', self.obj1), True)
        self.assertEquals(self.user1.has_perm('delete', self.obj1), True)

        # user2 doesn't have any permissions
        self.assertNotEquals(self.user2.has_perm('view', self.obj1), True)
        self.assertNotEquals(self.user2.has_perm('change', self.obj1), True)
        self.assertNotEquals(self.user2.has_perm('delete', self.obj1), True)
        
    """
    def test_duplicated_permission_object(self):
        # create permission object for user1
        ct = ContentType.objects.get_for_model(self.obj1)
        perm_obj = ObjectPermission.objects.create(user=self.user1,
                                                   content_type=ct, object_id=self.obj1.id,
                                                   can_view=True, can_change=True,
                                                   can_delete=True)
        perm_obj.save()
        
        # a ObjectPermission object has to be created
        self.assertEquals(ObjectPermission.objects.count(), 1)
        
        # check if user1 has view, change and delete permission
        self.assertEquals(self.user1.has_perm('view', self.obj1), True)
        self.assertEquals(self.user1.has_perm('change', self.obj1), True)
        self.assertEquals(self.user1.has_perm('delete', self.obj1), True)

        # create second permission object for the same user and object with different
        # permissions
        # creates an undefined state, use methods from utils to avoid!
        ct = ContentType.objects.get_for_model(self.obj1)
        perm_obj = ObjectPermission.objects.create(user=self.user1,
                                                   content_type=ct, object_id=self.obj1.id,
                                                   can_view=True, can_change=True,
                                                   can_delete=False)
        perm_obj.save()

        # object shouldn't been created
        self.assertEquals(ObjectPermission.objects.count(), 2)
    """
    def test_register_permission(self):
        self.assertEquals(grant_permissions(self.obj1, self.user1, ['view']), False)
        self.assertEquals(ObjectPermission.objects.count(), 0)
        self.assertEquals(PermissionType.objects.count(), 0)
        
        register(TestObj, 'view')
        self.assertEquals(PermissionType.objects.count(), 1)
        
        # create permissions with the add_permissions function
        self.assertEquals(grant_permissions(self.obj1, self.user1, ['view', 'change']), False)

        self.assertEquals(ObjectPermission.objects.count(), 0)
        self.assertEquals(self.user1.has_perm('view', self.obj1), False)
        self.assertEquals(self.user1.has_perm('change', self.obj1), False)


        self.assertEquals(grant_permissions(self.obj1, self.user1, ['view']), True)
        
        self.assertEquals(ObjectPermission.objects.count(), 1)
        self.assertEquals(self.user1.has_perm('view', self.obj1), True)
        self.assertEquals(self.user1.has_perm('change', self.obj1), False)

    def test_add_permission(self):
        register(TestObj, 'view')
        register(TestObj, 'change')
        register(TestObj, 'delete')
        
        # create permissions with the add_permissions function
        grant_permissions(self.obj1, self.user1, ['view'])

        self.assertEquals(ObjectPermission.objects.count(), 1)
        self.assertEquals(self.user1.has_perm('view', self.obj1), True)
        self.assertEquals(self.user1.has_perm('change', self.obj1), False)
        
        grant_permissions(self.obj1, self.user1, ['change'])
        
        self.assertEquals(ObjectPermission.objects.count(), 1)
        self.assertEquals(self.user1.has_perm('view', self.obj1), True)
        self.assertEquals(self.user1.has_perm('change', self.obj1), True)

        self.assertNotEquals(self.user1.has_perm('delete', self.obj1), True)


        self.assertNotEquals(self.user2.has_perm('view', self.obj1), True)
        self.assertNotEquals(self.user2.has_perm('change', self.obj1), True)
        self.assertNotEquals(self.user2.has_perm('delete', self.obj1), True)

    def test_add_permission_to_group(self):
        register(TestObj, 'view')
        register(TestObj, 'change')
        register(TestObj, 'delete')
        
        group = Group.objects.create(name='Group1')
        
        add_permission_to_group('view', group, self.obj1)
        add_user_to_group(self.user1, group)
        self.assertEquals(GroupObjectPermission.objects.count(), 1)
        self.assertEquals(self.user1.has_perm('view', self.obj1), True)
        self.assertEquals(self.user1.has_perm('invalid', self.obj1), False)
