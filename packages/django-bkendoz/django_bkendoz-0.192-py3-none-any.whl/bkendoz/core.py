from django.conf import settings
from django.utils.translation import gettext_lazy as _


def bool_to_str(b):
    """ transform a boolean to Yes/No """
    return _("Oui") if b else _("Non")


def str_list_to_str(ls, separator=", ", model_field=None):
    """ transform a list into a strings separated by commas """
    s = ""
    cnt = len(ls)
    for i in range(0, cnt): 
        if model_field and hasattr(ls[i], model_field):
            s += getattr(ls[i], model_field)
        else:
            s += ls[i]

        if i < (cnt - 1):
            s += separator
    return s


def get_all_fields(model):
    """ return all fields and properties (@property) of a model """
    meta_fields = {f.name: f for f in model._meta.fields}
    prop_fields = [prop for prop in dir(
        model) if isinstance(getattr(model, prop), property)]
    return meta_fields, prop_fields


def get_model_fields(model, fields='__all__', verbose=True):
    """ return field list and a verbose_name if verbose == true """
    model_fields = []
    meta_fields, prop_fields = get_all_fields(model)

    def process_meta_field(field):
        if field != 'id':
            appended = field if not verbose else field, meta_fields[field].verbose_name
            model_fields.append(appended)

    def process_prop_field(field):
        if field != 'pk' and hasattr(model, 'VERBOSE_PROPERTIES'):
            appended = field if not verbose else field, model.VERBOSE_PROPERTIES[field]
            model_fields.append(appended)

    if fields == '__all__':
        for field in meta_fields:
            process_meta_field(field)
        for field in prop_fields:
            process_prop_field(field)
        return model_fields

    for field in fields:
        if field in meta_fields:
            process_meta_field(field)
        elif field in prop_fields:
            process_prop_field(field)
    return model_fields


def get_color_from_class(color_classes):
    """ TODO """
    color_palette = []
    for color_class in color_classes:
        for color_field in color_class.COLOR_FIELDS:
            for obj in color_class.objects.order_by(color_field):
            # for obj in color_class.objects.order_by('color').distinct('color'):
                color_palette.append(getattr(obj, color_field))
            return color_palette


def get_layout_data():
    """ retourne LAYOUT definit dans settings.py """
    return settings.LAYOUT

# def retrieve_models_data(request, models):
#    data = []
#    for m, n, t in models:
#       limit = n if n else 10
#       title = t if t else m._meta.verbose_name_plural

#       object_list = m.objects.all()[:limit]
#       url_list = get_object_urls(request, m)
#       data.append((object_list, url_list, title))
#       return data

# def get_models_urls(request, models):
#    models_urls = {}
#    for mod in models:
#       if mod.__name__ not in models_urls:
#          models_urls[mod.__name__] = get_object_urls(request, mod)
#          return models_urls

# def generate_lists_data(request, classes):
#    lists_data = []
#    for cl, objects, data in classes:
#       if 'title' in data:
#          title = data['title']
#       else:
#          title = cl._meta.verbose_name_plural

#          lists_data.append(
#             (
#                'dt-panel dt-' + cl.__name__.lower(),
#                title,
#                get_model_fields(cl, data['fields']),
#                objects,
#                get_object_urls(request, cl)
#             )
#          )
#          return lists_data

# return [field, field, ...]

