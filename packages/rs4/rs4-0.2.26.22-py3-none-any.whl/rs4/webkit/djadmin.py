from django.contrib import admin
from django.utils.safestring import mark_safe
from django.forms import Widget
from django.contrib.admin import SimpleListFilter
from django.db.models import Q, F, Count
from django.db.models.fields import NOT_PROVIDED
import mimetypes
from django.db import models
from django.core.exceptions import ValidationError
import datetime
import uuid
from rs4.attrdict import AttrDict

def set_title (title):
    admin.site.site_title = title
    admin.site.site_header = "{}".format (title)
    admin.site.index_title = "{} Management Console".format (title)

# widgets -----------------------------------------------------
def get_type (path):
    return mimemodels.guess_type (os.path.basename (path))[0]

def ImageWidget (width = 360):
    class _ImageWidget(Widget):
        def render(self, name, value, **noneed):
            return value and mark_safe ('<img src="{}" width="{}">'.format (value, width)) or 'No Image'
    return _ImageWidget

class LinkWidget(Widget):
    def render(self, name, value, **noneed):
        return value and mark_safe ('<a href="{}">{}</a> [<a href="{}" target="_blank">새창</a>]'.format (value, value, value)) or 'No Image'

def VideoWidget (video_width = 320, video_height = 240):
    class _VideoWidget(Widget):
        def render(self, name, value, **noneed):
            return value and mark_safe (
                '<video width="{}" height="{}" controls><source src="{}" type="{}"></video>'.format (
                    video_width, video_height, value, get_type (value)
                )
            ) or 'No Video'
    return _VideoWidget

class AudioWidget(Widget):
    def render(self, name, value, **noneed):
        return value and mark_safe ('<audio controls><source src="{}" type="{}"></audio>'.format (
            value, get_type (value)
            )
        ) or 'No Audio'


# filter prototypes -------------------------------------------
class CountFilter(SimpleListFilter):
    title = None
    parameter_name = None
    _countable_realted_name = None
    _filter = {}
    _options = [1,3,5,10,20,30]

    def create_action_count_filter (self):
        return [(i, 'Above {}'.format (i)) for i in self._options]

    def lookups (self, request, model_admin):
        return self.create_action_count_filter ()

    def queryset (self, request, queryset):
        value = self.value()
        if value:
            return queryset.select_related ().annotate (buy_count = Count (self._countable_realted_name, **self._filter)).filter (buy_count__gt = value)
        return queryset


class NullFilter (SimpleListFilter):
    title = None
    parameter_name = None
    _field_name = None
    _options = {'NULL': 'Null', 'NOTNULL': 'Not Null'}

    def lookups (self, request, model_admin):
        return [('t', self._options ['NULL']), ('f', self._options ['NOTNULL'])]

    def queryset (self, request, queryset):
        value = self.value()
        if value:
            return queryset.filter (**{'{}__isnull'.format (self._field_name): value == 't' and True or False})
        return queryset


class StackedInline (admin.StackedInline):
    can_delete = False
    show_change_link = True


# ModelAdmin -------------------------------------------
class ModelAdmin (admin.ModelAdmin):
    image_width = 320
    video_width = 320
    enable_add = True
    enable_delete = True
    enable_change = True

    list_per_page = 100
    list_max_show_all = 200

    def has_add_permission(self, request, obj=None):
        return self.enable_add

    def has_delete_permission(self, request, obj=None):
        return self.enable_delete

    def has_change_permission(self, request, obj=None):
        return self.enable_change

    def before_changelist_view (self, queryset, context):
        pass

    def changelist_view (self, request, extra_context = None):
        r = super ().changelist_view (request)
        if hasattr (r, 'context_data') and 'cl' in r.context_data:
            self.before_changelist_view (r.context_data ['cl'].queryset, r.context_data)
        return r

    def save_model (self, request, obj, form, change):
        return super().save_model(request, obj, form, change)

    def formfield_for_dbfield (self, db_field, request, **kwargs):
        if 'widget' not in kwargs:
            if db_field.name.endswith ('image'):
                kwargs ['widget'] = ImageWidget (self.image_width)
                return db_field.formfield(**kwargs)
            elif db_field.name.endswith ('video'):
                kwargs ['widget'] = VideoWidget (self.video_width)
                return db_field.formfield(**kwargs)
            elif db_field.name.endswith ('audio'):
                kwargs ['widget'] = AudioWidget
                return db_field.formfield(**kwargs)
            elif db_field.name.endswith ('url'):
                kwargs ['widget'] = LinkWidget
                return db_field.formfield(**kwargs)
        return super ().formfield_for_dbfield (db_field, request, **kwargs)


# abstract model -----------------------------------------------
TYPE_MAP = [
        (models.CharField, str, 'string'),
        ((models.IntegerField, models.AutoField), int, 'integer'),
        (models.FloatField, float, 'float'),
        (models.BooleanField, bool, 'boolean'),
        (models.DateTimeField, datetime.datetime, 'datetime'),
        (models.DateField, datetime.date, 'date'),
        (models.TimeField, datetime.time, 'time'),
        (models.UUIDField, uuid.UUID, 'uuid'),
    ]

class TableInfo:
    def __init__ (self, name, columns):
        self.name = name
        self.columns = columns
        self.pk = None

        for field in self.columns.values ():
            if field.pk:
                self.pk = field
                break

TZ_UTC = datetime.timezone.utc
def utcnow ():
    return datetime.datetime.now ().astimezone (TZ_UTC)

class Model (models.Model):
    _table_info_cache = {}

    class Meta:
        abstract = True

    @classmethod
    def get_table_info (cls):
        name = cls.get_table_name ()
        if name in cls._table_info_cache:
            return cls._table_info_cache [name]
        cls._table_info_cache [name] = TableInfo (name, cls.get_table_columns ())
        return cls._table_info_cache [name]

    @classmethod
    def get_table_name (cls):
        return cls._meta.db_table

    @classmethod
    def get_table_columns (cls):
        columns = {}
        for field in cls._meta.fields:
            field_type = None
            field_type_name = None
            for ftype, ptype, name in TYPE_MAP:
                if isinstance (field, ftype):
                    field_type = ptype
                    field_type_name = name
                    break

            columns [field.column] = AttrDict (dict (
                column = field.column,
                type = field_type,
                type_name = field_type_name,
                pk = field.primary_key,
                unique = field.unique,
                max_length = field.max_length,
                null = field.null,
                blank = field.blank,
                choices = field.choices,
                help_text = field.help_text,
                validators = field.validators,
                default = field.default,
                auto_now_add = field_type_name == 'datetime' and field.auto_now_add or False,
                auto_now = field_type_name == 'datetime' and field.auto_now or False
            ))

        return columns

    @classmethod
    def create (cls, payload):
        return cls.validate (payload, True)

    @classmethod
    def validate (cls, payload, create = False):
        ti = cls.get_table_info ()
        for field in ti.columns.values ():
            if field.type_name == 'datetime':
                if field.auto_now:
                    payload [field.column] = utcnow ()
                    continue
                if create and field.auto_now_add:
                    payload [field.column] = utcnow ()
                    continue

            if field.column not in payload:
                if create:
                    if field.pk:
                        continue
                    if not isinstance (field.default, NOT_PROVIDED):
                        payload [field.column] = field.default
                    if field.null is False:
                        raise ValidationError ('field {} is missing'.format (field.column))
                continue

            value = payload [field.column]
            if field.null is False and value is None:
                raise ValidationError ('field {} should not be NULL'.format (field.column))
            if field.blank is False and value == '':
                raise ValidationError ('field {} should not be blank'.format (field.column))

            if value is None:
                continue

            if field.type and not isinstance (value, field.type):
                raise ValidationError ('field {} type should be {}'.format (field.column, field.type_name))

            if value == '' and field.null:
                payload [field.column] = value = None
                continue

            if field.choices:
                if isinstance (field.choices [0], (list, tuple)):
                    choices = [item [0] for item in field.choices]
                else:
                    choices = field.choices
                if value not in choices:
                    raise ValidationError ('field {} has invalid value'.format (field.column))

            if field.validators:
                for validate_func in field.validators:
                    validate_func (value)

        for k in payload:
            if k not in ti.columns:
                raise ValidationError ('field {} is not valid field'.format (k))

        return payload
