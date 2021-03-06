# coding: utf-8
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

@register.filter(name='field_attr')
def field_attr(field, attr):
    if attr == "type":
        return field.field.widget.input_type
    else:
        return field.field.widget.attrs.get(attr, "")

@register.filter(name='field_attrs')
def field_attrs(field):
    attrs = []
    for name, attr in field.field.widget.attrs.items():
        attrs.append((name, attr))
    return attrs

@register.filter(name='pluriel')
def pluriel(num):
    return "s" if int(num) > 1 else ""

# Rechechr d'un attribut dans le dictionnaire des champs ou colonnes
@register.filter(name='attr_title')
def attr_title(dico, key):
    return dico[key].get("title", "")

@register.filter(name='attr_subtitle')
def attr_subtitle(dico, key):
    return dico[key].get("subtitle", "")

@register.filter(name='attr_td_class')
def attr_td_class(dico, key):
    return dico[key].get("td_class", "crudy-data-table__cell--text-center")

@register.filter(name='attr_class')
def attr_class(dico, key):
    return dico[key].get("class", "")

@register.filter(name='attr_style')
def attr_style(dico, key):
    return dico[key].get("style", "")

@register.filter(name='attr_type')
def attr_type(dico, key):
    return dico[key].get("type", "text")

@register.filter(name='attr_url')
def attr_url(dico, key):
    return dico[key].get("url", "")

@register.filter(name='attr_hide')
def attr_hide(dico, key):
    return dico[key].get("hide", "")

@register.filter(name='attr_tooltip')
def attr_tooltip(dico, key):
    return dico[key].get("tooltip", "")

@register.filter(name='attr_list')
def attr_list(dico, key):
    return dico[key].get("list", "[]")

@register.filter(name='attr_colored_number')
def attr_colored_number(dico, key):
    return dico[key].get("colored_number", False)

@register.filter(name='attr_sort')
def attr_sort(dico, key):
    return dico[key].get("sort", False)

@register.filter(name='attr_disabled')
def attr_disabled(dico, key):
    return dico[key].get("disabled", False)

@register.filter(name='whist_carte')
def whist_carte(jeu, carte):
    if int(jeu) <= int(carte):
        return jeu
    else:
        return int(carte) - (int(jeu) - int(carte) - 1)
