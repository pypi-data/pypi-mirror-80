# -*- coding: utf-8 -*-
import os.path

from django.db.models.fields.related import RelatedField
from django.forms import BooleanField

from djgentelella.cruds import utils
from django import template

from django.urls import (reverse, NoReverseMatch)  # django2.0
from django.db import models
from django.utils.html import escape
from django.utils.safestring import mark_safe

from djgentelella.utils import get_settings, set_settings

register = template.Library()
if hasattr(register, 'assignment_tag'):
    register_tag = register.assignment_tag
else:
    register_tag = register.simple_tag


@register.filter
def get_attr(obj, attr):
    """
    Filter returns obj attribute.
    """
    return getattr(obj, attr)


@register_tag
def crud_url(obj, action, namespace=None):
    try:
        nurl = utils.crud_url_name(type(obj), action)
        if namespace:
            nurl = namespace + ':' + nurl
        if action in utils.LIST_ACTIONS:
            url = reverse(nurl)
        else:
            url = reverse(nurl, kwargs={'pk': obj.pk})
    except NoReverseMatch:
        url = None
    return url


@register_tag
def crud_inline_url(obj, inline, action, namespace=None):
    try:
        nurl = utils.crud_url_name(type(inline), action)
        if namespace:
            nurl = namespace + ':' + nurl
        if action in ['delete', 'update']:
            url = reverse(nurl, kwargs={'model_id': obj.pk,
                                        'pk': inline.pk})
        else:
            url = reverse(nurl, kwargs={'model_id': obj.pk})
    except NoReverseMatch:
        url = None
    return url


@register.filter
def format_value(obj, field_name):
    """
    Simple value formatting.

    If value is model instance returns link to detail view if exists.
    """
    if '__' in field_name:
        related_model, field_name = field_name.split('__', 1)
        obj = getattr(obj, related_model)
    display_func = getattr(obj, 'get_%s_display' % field_name, None)
    if display_func:
        return display_func()
    value = getattr(obj, field_name)

    if value.__class__.__name__ == 'ManyRelatedManager':
        return format_many_values(obj, field_name)

    if isinstance(value, models.fields.files.FieldFile):
        if value:
            return mark_safe('<a href="%s">%s</a>' % (
                value.url,
                os.path.basename(value.name),
            ))
        else:
            return ''

    if isinstance(value, models.Model):
        url = crud_url(value, utils.ACTION_UPDATE)
        if url:
            return mark_safe('<a href="%s">%s</a>' % (url, escape(value)))
        else:
            if hasattr(value, 'get_absolute_url'):
                url = getattr(value, 'get_absolute_url')()
                return mark_safe('<a href="%s">%s</a>' % (url, escape(value)))
    if value is None:
        value = ""
    return value


@register.simple_tag
def format_many_values(obj, field_name, separator=', '):
    objects = getattr(obj, field_name).all()
    result = []

    for v in objects:
        url = crud_url(v, utils.ACTION_UPDATE)
        if url:
            res = mark_safe('<a href="%s">%s</a>' % (url, escape(str(v))))
        elif hasattr(v, 'get_absolute_url'):
            url = getattr(v, 'get_absolute_url')()
            res = mark_safe('<a href="%s">%s</a>' % (url, escape(str(v))))
        else:
            res = escape(str(v))

        result.append(res)

    all_values = mark_safe(separator.join(result))
    return all_values


@register.inclusion_tag('gentelella/cruds/crud_fields.html')
def crud_fields(obj, fields=None):
    """
    Display object fields in table rows::

        <table>
            {% crud_fields object 'id, %}
        </table>

    * ``fields`` fields to include

        If fields is ``None`` all fields will be displayed.
        If fields is ``string`` comma separated field names will be
        displayed.
        if field is dictionary, key should be field name and value
        field verbose name.
    """
    if fields is None:
        fields = utils.get_fields(type(obj))
    elif isinstance(fields, str):
        field_names = [f.strip() for f in fields.split(',')]
        fields = utils.get_fields(type(obj), include=field_names)

    return {
        'object': obj,
        'fields': fields,
    }


@register_tag
def get_fields(model, fields=None):
    """
    Assigns fields for model.
    """
    include = [f.strip() for f in fields.split(',')] if fields else None
    return utils.get_fields(
        model,
        include
    )

def render_boolean_field(obj_field):
    filter = (
        'true' if obj_field else 'false',
        "fa-check-square" if obj_field else 'fa-square-o'
    )
    return mark_safe("""<div class="text-center %s" ><i class="fa %s"></i></div>"""%filter)


@register.simple_tag
def show_object_field(obj, field, field_name):
    obj_field = getattr(obj, field)
    if isinstance(obj_field,  RelatedField):
        dev = format_many_values(obj, field)
    elif isinstance(obj_field, BooleanField):
        dev = render_boolean_field(obj_field)
    else:
        dev = format_value(obj, field)
    return dev

@register.simple_tag(takes_context=True)
def form_get_form_display(context, form, **kwargs):
    url_name = context['request'].resolver_match.url_name
    fnc_name = get_settings(url_name, none_asdefault=True)
    if fnc_name is None:
        fnc_name = 'as_inline'
        if not hasattr(form, fnc_name):
            fnc_name = 'as_table'
        set_settings(url_name, fnc_name)
    else:
        if not hasattr(form, fnc_name):
            fnc_name = 'as_table'
    fnc = getattr(form, fnc_name)
    return fnc

@register.simple_tag(takes_context=True)
def icon_fa_tag(context, icon_name, **kwargs):
    icon="fa fa-meh-o"
    if icon_name == "delete":
        icon="fa fa-times"
    elif icon_name == "create":
        icon = 'fa fa-plus-circle'
    elif icon_name == "submit" or icon_name == "save":
        icon = 'fa fa-floppy-o'
    elif icon_name == "edit":
        icon = 'fa fa-pencil-square-o'
    elif icon_name == "cancel":
        icon = 'fa fa-ban'
    elif icon_name == "show":
        icon= 'fa fa-eye'
    elif icon_name == "accept":
        icon= 'fa fa-check'
    icon_result="<i class='"+icon+"'></i>"
    return mark_safe(icon_result)