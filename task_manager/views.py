from django.urls import path
from django.views.generic import TemplateView

class HomeView(TemplateView):
    template_name = "index.html"

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
]
