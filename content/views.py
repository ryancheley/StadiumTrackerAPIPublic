from django.shortcuts import render
from django.views.generic import TemplateView
from content.models import Content


class ContentTemplateView(TemplateView):
    model = Content
    template_name = 'page.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        if 'name' in self.kwargs.keys():
            title = self.kwargs['name']
        else:
            title = 'Home'
        data['pages'] = Content.objects.get(title=title)
        return data
