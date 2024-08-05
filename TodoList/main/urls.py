from django.urls import path
from .views import task_list, TaskDetail, TaskCreate, TaskUpdate, TaskDelete, CustomLoginView, RegisterPage, TaskAssign, TaskRevoke
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('task/<int:pk>/assign/', TaskAssign.as_view(), name='task-assign'),
    path('task/<int:pk>/revoke/', TaskRevoke.as_view(), name='task-revoke'),
    path('login/', CustomLoginView.as_view(), name ='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name ='logout'),
    path('register/', RegisterPage.as_view(), name ='register'),
    path('', task_list.as_view(), name='tasks'),
    path('task/<int:pk>/', TaskDetail.as_view(), name='task'),
    path('task-create/', TaskCreate.as_view(), name='task-create'),
    path('task-update/<int:pk>/', TaskUpdate.as_view(), name='task-update'),
    path('task-delete/<int:pk>/', TaskDelete.as_view(), name='task-delete'),
]