from django.views.generic import TemplateView
from django.shortcuts import render
from django.views.defaults import page_not_found, server_error


class HomeView(TemplateView):
    template_name = "index.html"

def handler404(request, exception):
    return page_not_found(request, exception, template_name='404.html')

def handler500(request):
    return server_error(request, template_name='500.html')

#from django.http import HttpResponse
#from django.views import View

#class HomeView(View):
#    def get(self, request):
#        return HttpResponse("Тестовая страница: Приложение работает!")