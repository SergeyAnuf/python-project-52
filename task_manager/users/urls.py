from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.UserListView.as_view(), name='users'),
    path('create/', views.UserCreateView.as_view(), name='register'),
    path(
        '<int:pk>/update/',
        views.UserUpdateView.as_view(),
        name='user_update'
    ),
    path('<int:pk>/delete/',
         views.UserDeleteView.as_view(),
         name='user_delete'
         ),
]

