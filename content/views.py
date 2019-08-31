from django.shortcuts import render
from django.views.generic import TemplateView
from content.models import Content


class ContentTemplateView(TemplateView):
    template_name = 'page.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['pages'] = Content.objects.get(pk=1)
        return data
