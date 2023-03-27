
from main import views
from django.urls import path, include


app_name = 'main'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('task/new/', views.new_task, name='new_task'),
    path('task/edit/<int:task_id>/', views.edit_task, name='edit_task'),
    path('task/delete/<int:task_id>/', views.delete_task, name='delete_task'),
    path('task/<int:task_id>/loop', views.loop_dashboard, name='loop_dashboard'),
    path('loop/new/<int:task_id>', views.new_loop, name='new_loop'),
    path('loop/edit/<int:loop_id>/', views.edit_loop, name='edit_loop'),
    path('task/result/<int:task_id>/',
         views.get_result, name='get_result'),
    path('task/result/download/file/<int:result_id>',
         views.download_file, name='download_file'),
    path('task/result/download/video/<int:task_id>',
         views.download_video, name='download_video'),
    path('task/result/download/file/all/<int:task_id>',
         views.download_all_file, name='download_all_file'),
    path('task/result/download/file/raw/<int:task_id>',
         views.download_raw_file, name='download_raw_file'),
    path('detection/<int:task_id>/', views.call_detect, name='call_detect'),
    path('login', views.login_view, name='login'),
    path('signup', views.signup_view, name='signup'),
    path('logout', views.logout_view, name='logout'),
    path('home', views.home_page, name='home'),
    path('account', views.account_page, name='account_page'),
]
