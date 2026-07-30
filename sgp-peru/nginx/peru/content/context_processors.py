from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from newsletter.forms import NewsLetterForm
from inventory.filters import InventoryFilter
from providers.filters import ProviderEntityFilter
from content.forms import FilterSearchForm
from .models import menuList
from django.http import HttpResponse


def site_id(request):
    country = 'co'
    contry_request = get_current_site(request).id

    if contry_request == 3:
        country = 'co'
    if contry_request == 4:
        country = 'bo'
    if contry_request == 5:
        country = 'cl'
    if contry_request == 6:
        country = 'pe'

    return {
        "country": country,
    }

def mega_search(request):
    filterSearchForm = FilterSearchForm()
    title_search_inventory = InventoryFilter()
    name_search_provider = ProviderEntityFilter()

    return {
        "filterSearchForm": filterSearchForm,
        "title_search_inventory": title_search_inventory,
        "name_search_provider": name_search_provider
    }


def news_letter(request):
    news_letter_form = NewsLetterForm()

    return {
        "news_letter_form": news_letter_form,
    }


def menus(request):
    menu_search = menuList.objects.filter(
        site__id=get_current_site(request).id, Menu_Choice='B.S')
    menu_hamburguer = menuList.objects.filter(
        site__id=get_current_site(request).id, Menu_Choice='M.H').first
    menu_help = menuList.objects.filter(
        site__id=get_current_site(request).id, Menu_Choice='N.A').first
    menu_links = menuList.objects.filter(
        site__id=get_current_site(request).id, Menu_Choice='L.I').first
    menu_footer = menuList.objects.filter(
        site__id=get_current_site(request).id, Menu_Choice='S.F').first
    menu_redes = menuList.objects.filter(
        site__id=get_current_site(request).id, Menu_Choice='R.S').first

    return {
        'menu_search': menu_search,
        'menu_hamburguer': menu_hamburguer,
        'menu_help': menu_help,
        'menu_links': menu_links,
        'menu_footer': menu_footer,
        'menu_redes': menu_redes,
    }
