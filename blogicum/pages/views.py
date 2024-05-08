from django.views.generic import TemplateView
from django.shortcuts import render


class AboutPage(TemplateView):
    template_name = 'pages/about.html'


class RulesPage(TemplateView):
    template_name = 'pages/rules.html'


def error404(request, exception):
    return render(request, 'pages/404.html', status=404)


def error403(request, reason=''):
    return render(request, 'pages/403csrf.html', status=403)


def error500(request, *args, **kwargs):
    return render(request, 'pages/500.html', status=500)
