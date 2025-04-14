from django.urls import path
from . import views, consumers

urlpatterns = [
    path('', views.main_dashboard, name='main_dashboard'),
    path('usecases/', views.usecase_list, name='usecase_list'),
    path('usecases/new/', views.usecase_create, name='usecase_create'),
    path('hub/', views.hub_view, name='hub_view'),
    path('hub/go/<int:pk>/', views.hub_redirect, name='hub_redirect'),
    path('shell/', views.server_list, name='server_list'),
    path('shell/<int:pk>/', views.shell_terminal, name='shell_terminal'),
    path('shell/live/', views.interactive_shell, name='interactive_shell'),
    path('ws/shell/live/', consumers.InteractiveSSHConsumer.as_asgi()),
]
