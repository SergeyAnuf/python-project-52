from django.views.generic import TemplateView

class HomeView(TemplateView):
    template_name = "index.html"

#from django.http import HttpResponse
#from django.views import View

#class HomeView(View):
#    def get(self, request):
#        return HttpResponse("Тестовая страница: Приложение работает!")