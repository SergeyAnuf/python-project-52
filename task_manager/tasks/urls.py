from django.urls import path
from . import views
from django.contrib.auth import get_user_model

def check_users_exist(request):
    if not get_user_model().objects.exists():
        return redirect('tasks:list')
    return None


app_name = 'tasks'

urlpatterns = [
    path('', views.TaskListView.as_view(), name='list'),
    path('create/', views.TaskCreateView.as_view(), name='create'),
    path('<int:pk>/', views.TaskDetailView.as_view(), name='detail'),
    path('<int:pk>/update/', views.TaskUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.TaskDeleteView.as_view(), name='delete'),
]
