from django.template import Library
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

register = Library()

@register.filter(name='addclass')
def addclass(field, class_attr):
    return field.as_widget(attrs={'class': class_attr})

@register.simple_tag
def model_name(value):
    '''
    Django template filter which returns the verbose name of a model.
    '''
    if hasattr(value, 'model'):
        value = value.model

    return value._meta.verbose_name.title()


@register.simple_tag
def model_name_plural(value):
    '''
    Django template filter which returns the plural verbose name of a model.
    '''
    if hasattr(value, 'model'):
        value = value.model

    return value._meta.verbose_name_plural.title()

@register.simple_tag
def field_name(value, field):
    '''
    Django template filter which returns the verbose name of an object's,
    model's or related manager's field.
    '''
    if hasattr(value, 'model'):
        value = value.model

    return value._meta.get_field(field).verbose_name.title()

@register.filter(needs_autoescape=True)
def tpl_donneur(value, autoescape=True):
    '''
    Exemple de retour de code html
    '''
    if value == 1:
        result = '<td style="width: 10px;"><span class="fa fa-hand-o-right" title="le donneur pour ce tour"></span></td>'
    else:
        result = '<td style="width: 10px;">&nbsp;</span></td>'

    return mark_safe(result)

@register.filter(name="get_col")
def get_col(row, col_id):
    '''
    Retourne la valeur de la colonne de la row
    '''
    return row[col_id]
