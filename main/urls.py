
from main import views
from django.urls import path, include


app_name = 'main'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('task/new/', views.new_task, name='new_task'),
    path('task/edit/<int:task_id>/', views.edit_task, name='edit_task'),
    path('task/<int:task_id>/loop', views.loop_dashboard, name='loop_dashboard'),
    path('loop/new/<int:task_id>', views.new_loop, name='new_loop'),
    path('loop/edit/<int:loop_id>/', views.edit_loop, name='edit_loop'),
    path('task/result/<int:task_id>/',
         views.get_result, name='get_result'),
    path('detection/<int:task_id>/', views.call_detect, name='call_detect'),


]
# path('task/result/<int:task_id>/',
#      views.test_save_result, name='test_save_result'),
