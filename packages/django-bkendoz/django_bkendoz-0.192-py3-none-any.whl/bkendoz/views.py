# import {{{1
import json
import pyexcel

from django.http import JsonResponse
from django.conf import settings
from django.urls import path
from django.http import FileResponse
from django.urls import reverse_lazy
from django.shortcuts import render, redirect

from django.views.generic import DetailView, CreateView, UpdateView, DeleteView, ListView
from django.views.generic.base import View, TemplateView
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth import views as auth_views
from django.utils.translation import gettext_lazy as _

from .forms import get_generic_form, ImportXlsForm
from .core import get_color_from_class, get_layout_data, get_model_fields
from .models import GenericModel

# LOGIN {{{1
class GenericLoginView(auth_views.LoginView):
    extra_context = {
        'settings': settings,
        'test': 'test'
    }

# DASHBOARD {{{1
class GenericDashboardView(PermissionRequiredMixin, TemplateView):
    models = []
    template_name = 'genviews/dashboard.html'
    dflt_model_template = 'genviews/dashboard_tpl.html'
    list_cls = 'dashboard-list'
    auth = 'superuser'

    def __init__(self, **kwargs):
        assert hasattr(settings, 'DASH_LIST_COUNT'), f"DASH_LIST_COUNT non défini dans settings.py, il faut définir la valeur par default du nombre d'element à afficher dans le tableau de bord"
        self.permission_required = f'{self.auth}.dashboard'
        super().__init__(**kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['models'] = {}
        for m in self.models:
            model_dict = context['models'][m] = {}
            obj_count = m.get_view_data('dashboard', 'count') or settings.DASH_LIST_COUNT
            model_dict['title'] = m.get_view_data('dashboard', 'title')
            model_dict['html'] = m.get_view_data('dashboard', 'html') or self.dflt_model_template
            model_dict['menu'] = m.get_dash_menu()
            model_dict['fields'] = self.get_dash_fields(m)
            model_dict['list'] = m.objects.all()[:obj_count]

        context['layout_data'] = get_layout_data()
        context['settings'] = settings
        return context

    def get_dash_fields(self, model):
        view_struct_fields = model.get_view_data('dashboard')
        return get_model_fields(model, view_struct_fields)

# OMNIBAR {{{1
# class GenericOmnibarView(PermissionRequiredMixin, View):
class GenericOmnibarView(View):
    models = []
    auth = 'superuser'

    def __init__(self, **kwargs):
        self.permission_required = f'{self.auth}.omnibar'
        super().__init__(**kwargs)

    def get(self, request, *args, **kwargs):
        d = [] 
        
        for m in self.models:
            assert issubclass(m, GenericModel), f'{m.get_id()} Must inherit from GenericModel' 
            for o in m.objects.all():
                d.append({
                    'type': m.get_id(),
                    'handler': 'toDetail',
                    'param0': o.get_omnibar_ref(),
                    'param1': o.get_absolute_url()
                })
        return JsonResponse(d, safe=False)
        
# LIST {{{1
class GenericListView(PermissionRequiredMixin, ListView):
    template_name = 'genviews/list.html'
    template_list_name = 'genviews/table.html'
    list_cls = 'generic-list'
    fields = '__all__' 

    def __init__(self, **kwargs):
        assert hasattr(settings, 'FIELDMAP'), f"Pas de template FIELDMAP défini dans settings.py, il faut définir comment chaque field de la liste va s'afficher dans un template"
        self.current_app = self.model._meta.app_label
        self.permission_required = f'{self.current_app}.list_{self.model.__name__.lower()}'
        self.template_name = self.model.get_view_data('list', 'tpl') or self.template_name
        super().__init__(**kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['list_title'] = self.model.get_view_data('list', 'title')
        context['list_menu'] = self.model.get_list_menu()
        context['list_cls'] = self.list_cls
        context['fields'] = self.get_list_fields();
        context['html'] = self.model.get_view_data('list', 'html') or self.template_list_name

        context['settings'] = settings
        context['layout_data'] = get_layout_data()
        return context

    def get_list_fields(self):
        view_struct_fields = self.model.get_view_data('list')
        return get_model_fields(self.model, view_struct_fields)

# CREATE {{{1
class GenericCreateView(PermissionRequiredMixin, CreateView):
    template_name = 'genviews/form.html'
    color_classes = []

    def __init__(self, **kwargs):
        self.current_app = self.model._meta.app_label
        self.permission_required = f'{self.current_app}.add_{self.model.__name__.lower()}'
        self.template_name = self.model.get_view_data('create', 'html') or self.template_name

        if not self.form_class:
            self.form_class = self.create_generic_form()
            self.initial = {'model': self.model}
            # both fields and form_class not permitted
            self.fields = None
            super().__init__(**kwargs)

    def create_generic_form(self):
        view_struct_fields = self.model.get_view_data('create')
        return get_generic_form(self.model, view_struct_fields) 

    def get_context_data(self, **kwargs):
        if 'param' in self.kwargs and 'pk' in self.kwargs:
            self.initial = {
                self.kwargs['param']: self.kwargs['pk']
            }

        context = super().get_context_data(**kwargs)

        context['form_title'] = self.model.get_view_data('create', 'title')
        context['form_action'] = reverse_lazy(f"{self.current_app}:{self.model.__name__.lower()}-create")
        if len(self.color_classes) > 0:
            context['color_palette'] = get_color_from_class(self.color_classes)

        context['layout_data'] = get_layout_data()
        context['settings'] = settings
        return context

    def get_success_url(self):
        if self.success_url:
            return reverse_lazy(self.success_url)

        for v, args in (('detail', [self.object.pk]), ('list', None), ('create', None)):
            if self.model.get_view_data(v):
                url = f"{self.current_app}:{self.model.__name__.lower()}-{v}"
                return reverse_lazy(url, args=args)

# UPDATE {{{1
class GenericUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = 'genviews/form.html'
    color_classes = []

    def __init__(self, **kwargs):
        self.current_app = self.model._meta.app_label
        self.permission_required = f'{self.current_app}.change_{self.model.__name__.lower()}'

        self.template_name = self.model.get_view_data('update', 'html') or self.template_name

        if not self.form_class:
            self.form_class = self.create_generic_form()
            # both fields and form_class not permitted
            self.fields = None
            self.initial = {'model': self.model}
            super().__init__(**kwargs)

    def create_generic_form(self):
        view_struct_fields = self.model.get_view_data('update')
        return get_generic_form(self.model, view_struct_fields) 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['form_title'] = self.model.get_view_data('update', 'title')
        context['form_action'] = reverse_lazy(
          f"{self.current_app}:{self.model.__name__.lower()}-update", args=[self.object.pk])

        if len(self.color_classes) > 0:
            context['color_palette'] = get_color_from_class(self.color_classes)

        context['settings'] = settings
        context['layout_data'] = get_layout_data()
        return context

    def get_success_url(self):
        if self.success_url:
            return reverse_lazy(self.success_url)

        for v, args in (('detail', [self.object.pk]), ('list', None), ('create', None)):
            if self.model.get_view_data(v):
                url = f"{self.current_app}:{self.model.__name__.lower()}-{v}"
                return reverse_lazy(url, args=args)

# DETAIL {{{1
class GenericDetailView(PermissionRequiredMixin, DetailView):
    template_name = 'genviews/detail.html'

    def __init__(self, **kwargs):
        self.current_app = self.model._meta.app_label
        self.permission_required = f'{self.current_app}.detail_{self.model.__name__.lower()}'
        self.template_name = self.model.get_view_data('detail', 'tpl') or self.template_name
        super().__init__(**kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['html'] = self.model.get_view_data('detail', 'html') or None
        context['MEDIA_URL'] = settings.MEDIA_URL
        context['detail_menu'] = self.object.get_view_menu('detail')

        # TODO utile ??
        #if hasattr(self, 'actions_extra'):
        #    context['actions_extra'] = self.actions_extra

        #if hasattr(self, 'template_extra'):
        #    context['template_extra'] = self.template_extra

        context['settings'] = settings
        context['layout_data'] = get_layout_data()
        return context

# HISTORY {{{1
class GenericHistoryView(PermissionRequiredMixin, DetailView):
    template_name = 'genviews/history.html'

    def __init__(self, **kwargs):
        self.current_app = self.model._meta.app_label
        self.permission_required = f'{self.current_app}.history_{self.model.__name__.lower()}'
        self.template_name = self.model.get_view_data('history', 'tpl') or self.template_name
        super().__init__(**kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list_title'] = self.model.get_view_data('history', 'title')
        context['list_menu'] = self.object.get_view_menu('history')
        context['object_list'] = self.object.history.all()
        context['fields'] = get_model_fields(self.model, self.fields)
        context['html'] = self.model.get_view_data('history', 'html') or None

        context['settings'] = settings
        context['layout_data'] = get_layout_data()
        return context


# DELETE {{{1
class GenericDeleteView(PermissionRequiredMixin, DeleteView):
    template_name = 'genviews/delete.html'

    def __init__(self, **kwargs):
        self.current_app = self.model._meta.app_label
        self.permission_required = f'{self.current_app}.delete_{self.model.__name__.lower()}'
        self.template_name = self.model.get_view_data('delete', 'tpl') or self.template_name
        super().__init__(**kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = f"{self.current_app}:{self.model.__name__.lower()}-detail"

        context['html'] = self.model.get_view_data('delete', 'html') or None
        context['settings'] = settings
        context['layout_data'] = get_layout_data()
        return context

    def get_success_url(self):
        for v, args in (('list', None), ('create', None)):
            if self.model.get_view_data(v):
                url = f"{self.current_app}:{self.model.__name__.lower()}-{v}"
                return reverse_lazy(url, args=args)


# EXPORT XLS {{{1
class GenericExportxlsView(PermissionRequiredMixin, View):
    def __init__(self, **kwargs):
        self.current_app = self.model._meta.app_label
        self.permission_required = f'{self.current_app}.exportxls_{self.model.__name__.lower()}'
        super().__init__(**kwargs)

    def get(self, request, *args, **kwargs):
        if hasattr(self.model, 'get_excel_dict'):
            xls_file = pyexcel.save_as(dest_file_type="xls", adict=self.model.get_excel_dict())
            return FileResponse(xls_file, as_attachment=True,
                                    filename=f"{self.model.__name__.lower()}_export.xls")
        else: 
            tuple_fields = self.get_exportxls_fields();
            tuple_fields.reverse()
            if tuple_fields == '__all__':
                objects = self.model.objects.values()
            else:
                objects = self.model.objects.values(*tuple_fields)

            xls_file = pyexcel.save_as(dest_file_type="xls", records=objects)
            return FileResponse(xls_file, as_attachment=True,
                  filename=f"{self.model.__name__.lower()}_export.xls")

    def get_exportxls_fields(self):
        view_struct_fields = self.model.get_view_data('exportxls')
        return view_struct_fields


# IMPORT XLS {{{1
class GenericImportxlsView(PermissionRequiredMixin, FormView):
    template_name = 'genviews/import_xls.html'
    form_class = ImportXlsForm

#init {{{2
    def __init__(self, **kwargs):
        self.current_app = self.model._meta.app_label
        self.permission_required = f'{self.current_app}.importxls_{self.model.__name__.lower()}'
        super().__init__(**kwargs)

#get context data {{{2
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = f"Importer des données excel"
        context['form_subtitle'] = self.model._meta.verbose_name
        context['fields'] = self.get_import_fields()
        context['import_sample'] = self.model.get_samples()
        context['layout_data'] = get_layout_data()
        context['settings'] = settings
        return context

    def get_import_fields(self):
        view_struct_fields = self.model.get_view_data('importxls')
        return get_model_fields(self.model, view_struct_fields)


#form_valid {{{2
    def form_valid(self, form):
        xls_file = form.files['xls_file']
      # print(pyexcel.get_sheet(file_type='xls', file_content=xls_file))
        records = pyexcel.get_records(file_type='xls', file_content=xls_file)

        context = self.get_context_data()
        context['preview'] = True
        context['object_list'] = self.model.create_object_list_from_records(
                records, self.fields)
        context['fields'] = get_model_fields(self.model, self.fields)
        context['model_plural'] = self.model._meta.verbose_name_plural
        context['form_action'] = f"{self.current_app}:{self.model.__name__.lower()}-importxlssave"

        return render(self.request, self.template_name,
              context=context)


#IMPORT XLS SAVE {{{1
class GenericImportxlssaveView(PermissionRequiredMixin, View):
    def post(self, request):
        for key, value in request.POST.items():
            if key.startswith("chk_"):
                if value == "off":
                    continue

                index = key.split("_")[1]
                data = json.loads(request.POST[index])
                m = self.model(**self.model.extract_json_dict(data))
                m.save()

        return redirect(reverse_lazy(f"{self.current_app}:{self.model.__name__.lower()}-list"))

#init {{{2
    def __init__(self, **kwargs):
        self.current_app = self.model._meta.app_label
        self.permission_required = f'{self.current_app}.importxlssave_{self.model.__name__.lower()}'
        super().__init__(**kwargs)

#   def form_valid(self, form):
#      def testinit(row):
#         # self.model.book_category.field.related_model
#         i = 0
#         new_row = []
#         for field_name in self.fields:
#            related_model = getattr(self.model, field_name).field.related_model
#            if related_model:
#               new_row.append(related_model.objects.get(pk=row[i]))
#            else:
#               new_row.append(row[i])
#            i = i + 1

#         print(new_row)
#         return new_row

#      xls_file = form.files['xls_file']
#      #print(pyexcel.get_sheet(file_type='xls', file_content=xls_file))
#      pyexcel.save_as(file_content=xls_file, file_type='xls',
#                            dest_initializer=testinit,
#                            dest_model=self.model,
#                       start_row=1,
#                       colnames=["book_category", "name"],
#                       dest_mapdict=["book_category", "name"]
#                      )

#      return super().form_valid(form)

#    def get_success_url(self):
#        if self.success_url:
#           return reverse_lazy(self.success_url)
#        else:
#           current_app = self.request.resolver_match.namespace
#           return reverse_lazy(f"{current_app}:{self.model.__name__.lower()}-importxls-preview")

##get {{{2
#   def get(self, request, *args, **kwargs):
#      if self.fields == '__all__':
#         objects = self.model.objects.values()
#      else:
#         objects = self.model.objects.values(*self.fields)

#      xls_file = pyexcel.save_as(dest_file_type="xls", records=objects)
#      response = FileResponse(xls_file, as_attachment=True,
#                              filename=f"{self.model.__name__.lower()}_import.xls")
#      return response
#      # return HttpResponse(xls_file, content_type="application/vnd.ms-excel")
#   pass

# create_model_paths {{{1
def create_model_paths(model):
    mod_name = model.__name__
    mod_name_low = mod_name.lower()
    path_to_return = []
# get_fields {{{
    def get_fields(view):
        fields = model.get_view_data(view.lower())
        if fields == '__all__':
            return get_model_fields(model)
        else:
            return fields
        if view == 'Exportxls':
            print(fields)
        return get_model_fields(model, fields)
# }}}

    assert issubclass(model, GenericModel), 'Not herited from GenericModel'
    assert hasattr(model, 'get_views_struct'), 'Not herited from GenericModel'

    for view in model.get_views_struct().keys():
        view = view.title()

        assert globals().get(f"Generic" + view + "View"), f"Error : trying to set generic views Generic{view}View for model {model}"

        # print(get_fields(view))
        # print(mod_name + view)
        ClassView = type(
              # name
              mod_name + view + "View", 
              # subclasses
              (globals()['Generic' + view + 'View'], ),
              # attr
              {
                  "model": model,
                  "fields": get_fields(view)
                  }
              )

        view_path = mod_name_low + 's/' + view.lower()
        if view in ['Update', 'Detail', 'Delete', 'History']:
            view_path += '/<int:pk>'

        path_to_return.append(
              path(
                  view_path,
                  ClassView.as_view(),
                  name=mod_name_low + '-' + view.lower()
                  )
              )

        if view == 'Create': 
            view_path += '/<str:param>/<int:pk>'
            path_to_return.append(
                  path(
                      view_path,
                      ClassView.as_view(),
                      name=mod_name_low + '-' + view.lower()
                      )
                  )
 
    return path_to_return
