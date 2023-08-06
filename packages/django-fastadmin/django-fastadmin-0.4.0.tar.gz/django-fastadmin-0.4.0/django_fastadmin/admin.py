import uuid
import copy
import json


from fastutils import listutils

from django.db import models
from django import forms
from django.forms import Textarea
from django.template.loader import render_to_string
from django.urls import reverse

from django.contrib import admin
from django.contrib.admin.options import BaseModelAdmin
from django.contrib.admin.options import InlineModelAdmin
from django.contrib.admin.options import csrf_protect_m
from django.contrib.admin.options import TO_FIELD_VAR
from django.contrib.admin.options import unquote

from django_middleware_global_request.middleware import get_request

from .utils import jquery_plugins


class UuidFieldSearchableAdmin(admin.ModelAdmin):
    """Enable search by uuid string with dashes.
    """
    def get_search_results(self, request, queryset, search_term):
        try:
            search_term_new = search_term
            if isinstance(search_term_new, str):
                search_term_new = search_term_new.strip()
            search_term_new = uuid.UUID(search_term_new).hex
        except ValueError:
            search_term_new = search_term
        result = super().get_search_results(request, queryset, search_term_new)
        return result



class InlineBooleanFieldsAllowOnlyOneCheckedMixin(InlineModelAdmin):
    """Admin inline formset has a boolean field, so that there are many checkboxes of that field, make sure that only one checkbox is checked.
    """

    special_class_name = "inline-boolean-fields-allow-only-one-checked-mixin"
    field_name_prefix = special_class_name + "-"

    class Media:
        js = jquery_plugins([
            "jquery/plugins/jquery.utils.js",
            "fastadmin/admins/inline-boolean-fields-allow-only-one-checked-mixin/inline-boolean-fields-allow-only-one-checked-mixin.js",
        ])


class InlineUniqueChoiceFieldsMixin(InlineModelAdmin):
    """ @todo
    """
    special_class_name = "with-inline-unique-choice-fields"
    field_name_prefix = special_class_name + "-"

    class Media:
        js = jquery_plugins([
            "jquery/plugins/jquery.utils.js",
            "fastadmin/admins/with-inline-unique-choice-fields.js",
        ])





class DisableInlineEditingInAddingMixin(BaseModelAdmin):
    """Disable inline editing in main object adding step.
    """
    def get_inline_instances(self, request, obj=None):
        if not obj or not obj.pk:
            return []
        else:
            return super().get_inline_instances(request, obj)


class InlineEditingHideOriginalMixin(BaseModelAdmin):
    """Hide original part in inline editing.
    """
    class Media:
        css = {
            "all": [
                "fastadmin/admins/inline-editing-hide-original-mixin/inline-editing-hide-original-mixin.css",
            ]
        }


class DisableDeleteActionMixin(BaseModelAdmin):
    """Disable delete action for all user.
    """
    DELETE_ACTION_ENABLE_FOR_SUPERUSER = False

    def get_actions(self, request):
        actions = super().get_actions(request)
        if request.user and request.user.is_superuser and self.DELETE_ACTION_ENABLE_FOR_SUPERUSER:
            pass
        else:
            if "delete_selected" in actions:
                del actions["delete_selected"]
        return actions



class DisableAddPermissionMixin(BaseModelAdmin):
    ADD_PERMISSION_ENABLE_FOR_SUPERUSER = False

    def has_add_permission(self, request):
        if not request.user:
            return False
        if not request.user.is_superuser:
            return False
        if not self.ADD_PERMISSION_ENABLE_FOR_SUPERUSER:
            return False
        return True

class DisableDeletePermissionMixin(BaseModelAdmin):
    DELETE_PERMISSION_ENABLE_FOR_SUPERUSER = False

    def has_delete_permission(self, request, obj=None):
        if not request.user:
            return False
        if not request.user.is_superuser:
            return False
        if not self.DELETE_PERMISSION_ENABLE_FOR_SUPERUSER:
            return False
        return True

class DisableChangePermissionMixin(BaseModelAdmin):
    CHANGE_PERMISSION_ENABLE_FOR_SUPERUSER = False

    def has_change_permission(self, request, obj=None):
        if not request.user:
            return False
        if not request.user.is_superuser:
            return False
        if not self.CHANGE_PERMISSION_ENABLE_FOR_SUPERUSER:
            return False
        return True


class MarkPermissionsMixin(BaseModelAdmin):

    def get_changing_object(self, request, object_id):
        if not object_id:
            return None
        else:
            to_field = request.POST.get(TO_FIELD_VAR, request.GET.get(TO_FIELD_VAR))
            obj = self.get_object(request, unquote(object_id), to_field)
            return obj

    @csrf_protect_m
    def changeform_view(self, request, object_id=None, form_url="", extra_context=None):
        obj = self.get_changing_object(request, object_id)
        extra_context = extra_context or {}
        has_add_permission = self.has_add_permission(request)
        has_view_permssion = self.has_view_permission(request, obj)
        has_change_permission = self.has_change_permission(request, obj)
        has_delete_permission = self.has_delete_permission(request, obj)
        setattr(request, "has_add_permission", has_add_permission)
        setattr(request, "has_view_permssion", has_view_permssion)
        setattr(request, "has_change_permission", has_change_permission)
        setattr(request, "has_delete_permission", has_delete_permission)
        extra_context.update({
            "has_add_permission": has_add_permission,
            "has_view_permssion": has_view_permssion,
            "has_change_permission": has_change_permission,
            "has_delete_permission": has_delete_permission,
        })
        return super().changeform_view(request, object_id, form_url, extra_context)


class TextFieldAutoHeightMixin(BaseModelAdmin):
    class Media:
        js = jquery_plugins([
            "fastadmin/admins/text-field-auto-height-mixin/text-field-auto-height-mixin.js",
        ])

class TextFieldSetRowColumnMixin(BaseModelAdmin):
    TEXT_AREA_ROW = 1
    TEXT_AREA_COLS = 80

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if models.TextField in self.formfield_overrides:
            self.formfield_overrides[models.TextField]["widget"] = Textarea(attrs={'rows': self.TEXT_AREA_ROW, 'cols': self.TEXT_AREA_COLS})




class DisplayField(object):

    template_name = None
    css = {}
    js = []

    def __init__(self, field_name, short_description, help_text=None):
        self.field_name = field_name
        self.short_description = short_description
        self.help_text = help_text

    def __call__(self, obj):
        request = get_request()
        templates = self.get_templates(request, obj)
        context = self.get_context(request, obj)
        return render_to_string(templates, context)

    def get_templates(self, request, obj):
        app_label = obj._meta.app_label
        model_name = obj._meta.model_name
        templates = [
            "admin/{}/{}/{}".format(app_label, model_name, self.template_name),
            "admin/{}/{}".format(app_label, self.template_name),
            "admin/{}".format(self.template_name),
        ]
        return templates

    def get_context(self, request, obj=None):
        add = request.path.endswith("/add/")
        app_label = obj._meta.app_label
        model_name = obj._meta.model_name
        context = {
            "request": request,
            "obj": obj,
            "field_name": self.field_name,
            "short_description": self.short_description,
            "help_text": self.help_text,
            "add": add,
            "has_change_permission": request.has_change_permission,
            "value": getattr(obj, self.field_name),
        }
        return context

class WithDisplayFieldsMixin(MarkPermissionsMixin):

    def get_display_fields_map(self):
        fields_map = {}
        for name in dir(self):
            if name in ["media"]:
                continue
            field = getattr(self, name)
            if isinstance(field, DisplayField):
                fields_map[field.field_name] = name
        return fields_map

    def get_fieldsets(self, request, obj=None):
        fields_map = self.get_display_fields_map()
        fieldsets = super().get_fieldsets(request, obj)
        fieldsets = copy.deepcopy(fieldsets)
        if request.method != 'POST':
            for block in fieldsets:
                fields = listutils.replace(block[1]["fields"], fields_map)
                block[1]["fields"] = fields
        return fieldsets

    def get_readonly_fields(self, request, obj=None):
        fields_map = self.get_display_fields_map()
        fields = list(super().get_readonly_fields(request, obj))
        fields = copy.deepcopy(fields)
        for field_old, field_new in fields_map.items():
            if not field_new in fields:
                fields.append(field_new)
        return fields

    @property
    def media(self):
        resource = super().media
        fields_map = self.get_display_fields_map()
        for _, display_field_name in fields_map.items():
            field = getattr(self, display_field_name)
            resource += forms.Media(css=field.css, js=field.js)
        return resource
    

class HideShowField(DisplayField):
    template_name = "hide_show_field.html"
    css = {
        "all": [
            "fastadmin/admins/hide-show-field/hide-show-field.css",
        ]
    }
    js = jquery_plugins([
        "fastadmin/admins/hide-show-field/hide-show-field.js",
    ])

class EditablePasswordField(DisplayField):

    template_name = "fastadmin/admins/editable-password-field/editable-password-field.html"
    css = {
        "all": [
            "fastadmin/admins/editable-password-field/editable-password-field.css",
        ]
    }
    js = jquery_plugins([
        "fastadmin/admins/editable-password-field/editable-password-field.js",
    ])


class ResetToRandomPasswordField(object):

    template_name = "fastadmin/admins/reset-to-random-password-field/reset-to-random-password-field.html"
    css = {
        "all": [
            "fastadmin/admins/reset-to-random-password-field/reset-to-random-password-field.css",
        ]
    }
    js = jquery_plugins([
        "fastadmin/admins/reset-to-random-password-field/reset-to-random-password-field.js",
    ])

    def __init__(self, field_name, get_password_url, short_description, help_text=None, params=None):
        super().__init__(field_name, short_description, help_text)
        self.get_password_url = get_password_url
        self.params = params

    def get_context(self, request, obj=None):
        context = super().get_context(request, obj)
        context.update({
            "get_password_url": reverse(self.get_password_url),
            "params": self.params,
            "params_json": json.dumps(self.params),
        })
        return context

