import json
import importlib

from django.db import models
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from simple_history.models import HistoricalRecords

# GenericModel {{{1
class GenericModel(models.Model):
    LINK_FIELD = 'name'

    # Meta {{{2
    class Meta:
        abstract = True

    @classmethod
    def get_id(cls):
        return cls.__name__.lower()

    # get_views_struct {{{2
    @classmethod
    def get_views_struct(cls):
        assert hasattr(cls, 'views_struct'), f"GenericModel without a views dict 'views_struct' for model {cls} !"
        return cls.views_struct

    # get_view_data {{{2
    @classmethod
    def get_view_data(cls, view, prop='fields'):
        if view not in cls.get_views_struct():
            print(f"structure pour {cls} vue : {view} non defini")
            return None
        
        if prop not in cls.get_views_struct()[view]:
            if prop == 'fields':
                return '__all__'

            if view == 'create' and prop == 'title':
                return _("Nouveau") + " " + \
                    cls._meta.verbose_name.lower()

            print(f"propriete {prop} non definie pour {cls} vue : {view}")
            return None

        return cls.get_views_struct()[view][prop]

    # get_list_menu {{{2
    @classmethod
    def get_list_menu(cls):
        views_struct = cls.get_views_struct()
        assert 'list' in views_struct, f"No list view for {cls}"
        assert 'menu' in views_struct['list'], f"No menu in listview for {cls}"

        list_menu = []
        for model_ref, view_name, faclass, url_args in views_struct['list']['menu']:
            list_menu.append( (cls.get_url(view_name.lower()), faclass) )
        return list_menu

    # get_dash_menu {{{2
    @classmethod
    def get_dash_menu(cls):
        views_struct = cls.get_views_struct()
        assert 'dashboard' in views_struct, f"No dashboard view for {cls}"
        assert 'menu' in views_struct['dashboard'], f"No menu in dashboardview for {cls}"

        dashboard_menu = []
        for model_ref, view_name, faclass, url_args in views_struct['dashboard']['menu']:
            dashboard_menu.append( (cls.get_url(view_name.lower()), faclass) )
        return dashboard_menu

    # # get_detail_menu {{{2
    # def get_detail_menu(self):
    #     assert 'detail' in self.__class__.get_views_struct(), f"No detail view for {self.__class__}"
    #     assert 'menu' in self.__class__.get_views_struct()['detail'], f"No detail menu for {self.__class__}"

    #     detail_menu = []

    #     for model_ref, view_name, faclass, url_args in self.__class__.get_views_struct()['detail']['menu']:

    #         module_name, class_name = model_ref.split(':')
    #         module = importlib.import_module(module_name) 
    #         model = getattr(module, class_name)

    #         kwargs = {}
    #         for self_field, other_field in url_args:
    #             if not other_field:
    #                 if not hasattr(model, self_field):
    #                     print(f"Warning : trying to acces non existent url arg {field} in {self.__class__} when generating detail menu")
    #                     continue
    #                 kwargs[self_field] = getattr(self, self_field)
    #             else:
    #                 assert hasattr(self, self_field)
    #                 assert hasattr(model, other_field)
    #                 kwargs['param'] = other_field
    #                 kwargs['pk'] = getattr(self, self_field)

    #         href = reverse_lazy(model.get_url(view_name.lower()), kwargs=kwargs)
    #         detail_menu.append( (href, faclass) )
    #     return detail_menu

    # get_view_menu {{{2
    def get_view_menu(self, view):
        assert view in self.__class__.get_views_struct(), f"No {view} view for {self.__class__}"
        assert 'menu' in self.__class__.get_views_struct()[view], f"No {view} menu for {self.__class__}"

        menu = []

        struct_menu = self.__class__.get_views_struct()[view]['menu'] 
        for model_ref, view_name, faclass, url_args in struct_menu:
            module_name, class_name = model_ref.split(':')
            module = importlib.import_module(module_name) 
            model = getattr(module, class_name)

            kwargs = {}
            for self_field, other_field in url_args:
                if not other_field:
                    if not hasattr(model, self_field):
                        print(f"Warning : trying to acces non existent url arg {field} in {self.__class__} when generating detail menu")
                        continue
                    kwargs[self_field] = getattr(self, self_field)
                else:
                    assert hasattr(self, self_field)
                    assert hasattr(model, other_field)
                    kwargs['param'] = other_field
                    kwargs['pk'] = getattr(self, self_field)

            href = reverse_lazy(model.get_url(view_name.lower()), kwargs=kwargs)
            menu.append( (href, faclass, None, None) )

        if 'extra_menu' in self.__class__.get_views_struct()[view]:
            extras = self.__class__.get_views_struct()[view]['extra_menu']
            for href, faclass, aclass, data in extras:
                menu.append( (href, faclass, aclass, data) )

        return menu

    # get_url {{{2
    @classmethod
    def get_url(cls, view_name):
        assert view_name in cls.get_views_struct().keys(), f"trying to reverse url with a view not specified in views_struct for {cls} with view {view_name}"
        return f"{cls._meta.app_label}:{cls.__name__.lower()}-" + view_name


    # # get_fields_data {{{2
    # @classmethod
    # def get_fields_data(cls, fieldlist):
    #     field_data = []
    #     for field in fieldlist:
    #         if not hasattr(cls, field):
    #             continue
    #         field_data.append( (field, getattr(cls, field).field.verbose_name) )
    #     print(field_data)
    #     return field_data

    # extract json dict {{{2
    @classmethod
    def extract_json_dict(cls, json):
        kwargs = {}
        for key,value in json.items():
            related_model = getattr(cls, key).field.related_model
            if related_model:
                kwargs[key] = related_model.objects.get(pk=value)
            else:
                kwargs[key] = value
        return kwargs
 
 
    # extract excel record dict {{{2
    @classmethod
    def extract_record_dict(cls, record):
        kwargs = {}
        for field in record:
            related_model = getattr(cls, field).field.related_model
            if related_model:
                kwargs[field] = related_model.objects.get(pk=record[field])
            else:
                kwargs[field] = record[field]
        return kwargs

    # create object list from excel records {{{2
    @classmethod
    def create_object_list_from_records(cls, records, fields):
        object_list = []
        index = 0
        print(records)
        print(fields)
        for record in records:
            print(record)
            o = cls(**cls.extract_record_dict(record))
            o_dict = {}
            for field in fields:
                related_model = getattr(cls, field).field.related_model
                if related_model:
                    o_dict[field] = getattr(o, field).pk
                else:
                    o_dict[field] = getattr(o, field)
            o.json = json.dumps(o_dict)
            o.index = index
            index += 1
            object_list.append(o)
        return object_list


    # get samples {{{2
    # @classmethod
    # def get_samples(cls):
    #     return [cls(), cls()]
    
    # get omnibar ref {{{2
    def get_omnibar_ref(self):
        cls = self.__class__
        f = cls.get_view_data('omnibar') 
        if f:
            return getattr(self, f)
        elif hasattr(self, 'name'):
            return self.name
        else:
            return str(self)

    # get absolute url {{{2
    def get_absolute_url(self):
        app = self.__class__._meta.app_label.lower()
        model = str(self.__class__.__name__).lower()

        if 'detail' in self.__class__.get_views_struct():
            return reverse_lazy(f"{app}:{model}-detail", args=[str(self.id)])

        if 'list' in self.__class__.get_views_struct():
            return reverse_lazy(f"{app}:{model}-list")

# GenericHistorizedModel {{{1
class GenericHistorizedModel(GenericModel):
    history = HistoricalRecords(inherit=True)

    @property
    def hist_date(self):
        return self.history_date

    class Meta:
        abstract = True

# GenericExcelModel {{{1
class GenericExcelModel:
    pass
