from django import template
from django.forms.formsets import formset_factory
from django.utils.translation import ugettext_lazy as _
from django.forms.formsets import formset_factory, BaseFormSet
from united_geonames.forms import UserGeoNameForm, DatabaseForm
from django.template import Context, loader
register = template.Library()


@register.simple_tag(takes_context=True)
def user_form(context, parameter):
    # atvaizduojam forma tik puslapyje, kuris turi id: search_hpn
    if parameter == 'search_hpn':
        user_geo_name_form = UserGeoNameForm()
        request = context['request']
        if request.method == 'POST':
            if not rp['coordinates_lat'] and not rp['coordinates_lon']:
                user_geo_name_form = UserGeoNameFormWithoutMap(request.POST)
            else:
                user_geo_name_form = UserGeoNameForm(request.POST)
        else:
            context['user_geo_name_form'] = user_geo_name_form
            return loader.get_template('tags/forms/user_form.html').render(context)
    else:
        return ''

@register.simple_tag(takes_context=True)
def load_anycluster(context, parameter):
    if parameter == 'hpn_menu':
        return loader.get_template('tags/anycluster.html').render(context)
    else:
        return ''

@register.simple_tag(takes_context=True)
def database_form(context, parameter):
    if parameter == 'database':
        context['database_form'] = DatabaseForm()
        return loader.get_template('tags/forms/database_form.html').render(context)
    else:
        return ''