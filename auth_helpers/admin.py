import settings
from django import forms
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType

from .auth.models import PermissionType, ObjectPermission, GroupObjectPermission


def create_user_permission_obj(modeladmin, request, queryset):
    for obj in queryset:
         ct = ContentType.objects.get_for_model(obj)
         perm_obj = ObjectPermission.objects.create(content_type=ct,
                                                    object_id=obj.id)

def create_group_permission_obj(modeladmin, request, queryset):
    for obj in queryset:
         ct = ContentType.objects.get_for_model(obj)
         perm_obj = GroupObjectPermission.objects.create(content_type=ct,
                                                         object_id=obj.id)

admin.site.add_action(create_user_permission_obj)
admin.site.add_action(create_group_permission_obj)


class ObjectPermissionForm(forms.ModelForm):

    permission_list = forms.MultipleChoiceField(required=False)
    
    def __init__(self, *args, **kwargs):
        super(ObjectPermissionForm, self).__init__(*args, **kwargs)

        self.fields['permission_list'] = forms.MultipleChoiceField(required=False)
        
        permission_types = PermissionType.objects.filter(content_type=kwargs['instance'].content_type)

        choices = []
        cls_list = set()
        for pt in permission_types:
            choices.append([pt.permission_name,  '%s:%s' %( pt.content_type, pt.permission_name)])
           
        self.fields['permission_list'].choices = choices

        
    class Meta:
        model = ObjectPermission
   
    
class ObjectPermissionAdmin(admin.ModelAdmin):
    form = ObjectPermissionForm

class GroupObjectPermissionForm(forms.ModelForm):

     permission_list = forms.MultipleChoiceField(required=False)

     def __init__(self, *args, **kwargs):
         super(GroupObjectPermissionForm, self).__init__(*args, **kwargs)

         self.fields['permission_list'] = forms.MultipleChoiceField(required=False)

         permission_types = PermissionType.objects.filter(content_type=kwargs['instance'].content_type)

         choices = []
         cls_list = set()
         for pt in permission_types:
             choices.append([pt.permission_name,  '%s:%s' %( pt.content_type, pt.permission_name)])

         self.fields['permission_list'].choices = choices


     class Meta:
         model = GroupObjectPermission

class GroupObjectPermissionAdmin(admin.ModelAdmin):
    form = GroupObjectPermissionForm


class GroupObjectPermissionAdmin(admin.ModelAdmin):
     form = GroupObjectPermissionForm

class PermissionTypeAdmin(admin.ModelAdmin):
    pass

admin.site.register(ObjectPermission, ObjectPermissionAdmin)
admin.site.register(GroupObjectPermission, GroupObjectPermissionAdmin)
admin.site.register(PermissionType, PermissionTypeAdmin)

"""
class NonrelPermissionUserForm(UserForm):
    user_permissions = forms.MultipleChoiceField(required=False)
    groups = forms.MultipleChoiceField(required=False)
    
    def __init__(self, *args, **kwargs):
        super(NonrelPermissionUserForm, self).__init__(*args, **kwargs)

        self.fields['user_permissions'] = forms.MultipleChoiceField(required=False)
        self.fields['groups'] = forms.MultipleChoiceField(required=False)
        
        permissions_objs = Permission.objects.all().order_by('name')
        choices = []
        for perm_obj in permissions_objs:
            choices.append([perm_obj.id, perm_obj.name])
        self.fields['user_permissions'].choices = choices
        
        group_objs = Group.objects.all()
        choices = []
        for group_obj in group_objs:
            choices.append([group_obj.id, group_obj.name])
        self.fields['groups'].choices = choices

        try:
            user_perm_list = UserPermissionList.objects.get(
                user=kwargs['instance'])
            self.fields['user_permissions'].initial = user_perm_list.fk_list
        except (UserPermissionList.DoesNotExist, KeyError):
            self.fields['user_permissions'].initial = list()
            
        try:
            user_group_list = GroupList.objects.get(
                user=kwargs['instance'])
            self.fields['groups'].initial = user_group_list.fk_list
        except (GroupList.DoesNotExist, KeyError):
            self.fields['groups'].initial = list()


    

class NonrelPermissionCustomUserAdmin(UserAdmin):
    fieldsets = None
    form = NonrelPermissionUserForm
    
    def save_model(self, request, obj, form, change):
        super(NonrelPermissionCustomUserAdmin, self).save_model(request, obj, form, change)

        if len(form.cleaned_data['user_permissions']) > 0:
            permissions = list(Permission.objects.filter(
                id__in=form.cleaned_data['user_permissions']).order_by('name'))
        else:
            permissions = []

        update_permissions_user(permissions, obj)

        if len(form.cleaned_data['groups']) > 0:
            groups = list(Group.objects.filter(
                id__in=form.cleaned_data['groups']))
        else:
            groups = []

        update_user_groups(obj, groups)

"""




