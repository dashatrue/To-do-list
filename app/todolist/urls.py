from .views import *
from django.urls import path, include

urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('user/', user_tasks_list, name='user_tasks_list'),
    path('', category_list, name='category_list'),
    path('categories/create/', create_category, name='create_category'),
    path('categories/<int:category_id>/', category_tasks, name='category_tasks'),
    path('categories/delete/<int:category_id>/', delete_category, name='delete_category'),
    path('tasks/create/', create_task, name='create_task'),
    path('tasks/update/<int:task_id>/', update_task, name='update_task'),
    path('tasks/delete/<int:task_id>/', delete_task, name='delete_task'),
    path('task-chart/', task_chart, name='task_chart'),
]