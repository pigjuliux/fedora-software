from collections import Counter
from django.conf import settings
from django.shortcuts import render
from django.views.generic import TemplateView, DetailView

from .models import FeaturedApp, Component, Category


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self):
        featured_app    = FeaturedApp.objects.order_by('?').first()
        highlight_apps  = Component.objects.filter(
            type='desktop',
            type_id__in=settings.FS_HIGHLIGHT_APPS,
        ).exclude(id=featured_app.component.id).order_by('?')[:12]
        highlight_cats = Category.objects.filter(
            slug__in=settings.FS_HIGHLIGHT_CATS,
        ).exclude(id=featured_app.component.id).order_by('?')[:12]
        return {
            'featured_app':     featured_app,
            'highlight_apps':   highlight_apps,
            'highlight_cats':   highlight_cats,
        }



class AppView(DetailView):
    model           = Component
    template_name   = 'app.html'

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        return queryset.get(
            type='desktop',
            type_id='{}.desktop'.format(self.kwargs['id']),
        )

    def get_context_object_name(self, obj):
        return 'app'



class CategoryView(DetailView):
    model           = Category
    template_name   = 'category.html'

class SearchView(TemplateView):
    template_name = 'search.html'

    def get_context_data(self):
        # get query string from request
        q = self.request.GET.get('q')

        # find results
        apps = Component.objects.filter(type='desktop')
        apps_by_name    = apps.filter(names__name__contains=q).distinct()
        apps_by_summary = apps.filter(summaries__summary__contains=q).distinct()
        apps_by_desc    = apps.filter(descriptions__description__contains=q).distinct()
        apps_by_keyword = apps.filter(keywords__keyword__contains=q).distinct()

        # mix that together
        counter = Counter(apps_by_name)
        counter.update(apps_by_summary)
        counter.update(apps_by_desc)
        counter.update(apps_by_keyword)
        search_results = [mc[0] for mc in counter.most_common()]
        return {
            'search_query':     q,
            'search_results':   search_results,
        }

class FaqView(TemplateView):
    template_name = 'faq.html'

class UserView(TemplateView):
    template_name = 'user.html'
