from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login
from .models import Task



"""Выдача прав доступа к задаче другим пользователям"""
class TaskAssign(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Task
    template_name = 'main/task_assign.html'

    def post(self, request, *args, **kwargs):
        task = self.get_object()
        user_id = request.POST.get('user_id')
        if user_id:
            user = get_object_or_404(User, id=user_id)
            task.assigned_to = user
            task.save()
        return redirect('tasks')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = User.objects.all()
        return context

    def test_func(self):
        task = self.get_object()
        return self.request.user == task.user




"""Отзыв прав доступа к задаче других пользователей"""
class TaskRevoke(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Task
    template_name = 'main/task_revoke.html'

    def post(self, request, *args, **kwargs):
        task = self.get_object()
        task.assigned_to = None
        task.save()
        return redirect('tasks')

    def test_func(self):
        task = self.get_object()
        return self.request.user == task.user



""" Страница для входа пользователей """
class CustomLoginView(LoginView):
    template_name = 'main/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasks')
    

""" Страница для регистрации пользователей """
class RegisterPage(FormView):
    template_name = 'main/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('tasks')
    """Функция для автоматического входа пользователя в аккаунт после регистрации"""
    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)


"""Страница со всеми задачи пользователя(благодаря "LoginRequiredMixin" появляется запрет на просмотр страниц без авторизации)"""
class task_list(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'
    template_name = 'main/task_list.html'
    """Функция, благодаря которой у каждого пользователя будут выводиться задачи относящиеся к его аккаунту"""
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user) | context['tasks'].filter(assigned_to=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()
        return context


"""Просмотр конкретной задачи пользователя"""
class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'main/task.html'


"""Создание пользователем задачи"""
class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('tasks')
    """Функция запрещающая пользователю создавать записи другим людям"""
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)


"""Изменение пользователем задачи"""
class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('tasks')
    

"""Удаление пользователем задачи"""
class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')
    template_name = 'main/task_delete.html'