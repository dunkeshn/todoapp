from django.db import IntegrityError

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, TemplateView, DetailView, RedirectView, FormView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from . import models, forms, filters
from django.utils.timezone import now
from django.views.decorators.http import require_http_methods

from .models import Users


class Welcome(LoginRequiredMixin,
              TemplateView):
    template_name = 'core/welcome.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['authuser'] = self.request.user
        context['user'] = self.request.user
        return context


class Tasks(LoginRequiredMixin,
            ListView):
    template_name = 'core/tasks.html'
    model = models.Tasks
    context_object_name = 'tasks'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['authuser'] = self.request.user
        context['user'] = self.request.user
        context['tasks'] = models.Tasks.objects.filter(owners=self.request.user, completed=False)
        context['tasksdone'] = models.Tasks.objects.filter(owners=self.request.user, completed=True)
        return context


class AddingTask(View):
    def post(self, request):
        title = request.POST['title']
        if title:
            task = models.Tasks(title=title)
            task.save()
            task.owners.add(self.request.user)
            task.save()
        return redirect('tasks')


class DeletingTask(View):
    def get(self, request, task_id):
        task = models.Tasks.objects.get(id=task_id)
        task.delete()
        return redirect('tasks')


class DeletingTaskSearch(DeletingTask):
    def get(self, request, task_id):
        super().get(request,
                    task_id)
        return redirect('search')


class CompletingTask(View):
    def get(self, request, task_id):
        task = models.Tasks.objects.get(id=task_id)
        task.completed = not task.completed
        task.save()
        return redirect('tasks')


class CompletingTaskSearch(CompletingTask):
    def get(self, request, task_id):
        super().get(request,
                    task_id)
        return redirect('search')


class EditingTask(LoginRequiredMixin,
                  View):
    def get(self, request, task_id):
        task = models.Tasks.objects.get(id=task_id)
        users = task.owners.all()
        context = {'task': task, 'users': users, 'authuser': self.request.user}
        return render(request,
                      'core/edit_task.html',
                      context)


class UpdatingTask(View):
    def post(self, request, task_id):
        description = request.POST['description']
        task = models.Tasks.objects.get(id=task_id)
        task.description = description
        task.save()
        return redirect('tasks')


class UpdatingTaskSearch(UpdatingTask):
    def post(self, request, task_id):
        super().post(request,
                     task_id)
        return redirect('search')


class ChangingPriority(View):
    def get(self, request, task_id):
        task = models.Tasks.objects.get(id=task_id)
        if task.priority == 'COMMON':
            priority = 'LOW'
        elif task.priority == 'LOW':
            priority = 'MEDIUM'
        elif task.priority == 'MEDIUM':
            priority = 'HIGH'
        elif task.priority == 'HIGH':
            priority = 'COMMON'
        task.priority = priority
        task.save()
        return redirect('tasks')


class ChangingPrioritySearch(ChangingPriority):
    def get(self, request, task_id):
        super().get(request,
                    task_id)
        return redirect('search')


class Search(LoginRequiredMixin,
             TemplateView):
    template_name = 'core/tasksearch.html'
    model = models.Tasks
    context_object_name = 'search'

    def get_filters(self):
        return filters.Tasks(self.request.GET)

    def get_queryset(self):
        return self.get_filters().qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['authuser'] = self.request.user
        context['user'] = self.request.user
        context['tasks'] = self.get_queryset().filter(owners=self.request.user, completed=False)
        context['tasksdone'] = self.get_queryset().filter(owners=self.request.user, completed=True)
        context['filters'] = self.get_filters()
        return context


class Login(FormView):
    template_name = 'core/login.html'
    form_class = forms.LoginForm
    success_url = 'home'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request,
                                *args,
                                **kwargs)

    def post(self, request):
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['username']
            password = form.cleaned_data['password']
            usr = authenticate(request,
                               username=email,
                               password=password)
            if usr is not None:
                login(request,
                      usr)
                return redirect('tasks')
            else:
                notification = True
                return render(request, 'core/login.html', {'form': form, 'notification': notification})
        return render(request, 'core/login.html', {'form': form})


class Logout(TemplateView):
    def get(self, request):
        logout(request)
        return redirect('login')


class Registration(FormView):
    template_name = 'core/registration.html'
    form_class = forms.RegistrationForm
    success_url = 'home'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request,
                                *args,
                                **kwargs)

    def post(self, request):
        form = forms.RegistrationForm(request.POST)
        if form.is_valid():
            try:

                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']
                email = form.cleaned_data['email']
                username = form.cleaned_data['username']
                date_of_birth = form.cleaned_data['date_of_birth']
                picture = form.cleaned_data['picture']
                password = form.cleaned_data['password']
                submit_password = form.cleaned_data['submit_password']
                if password == submit_password:
                    Users.objects.create_user(username=username,
                                              password=password,
                                              first_name=first_name,
                                              last_name=last_name,
                                              picture=picture,
                                              email=email,
                                              date_of_birth=date_of_birth)

                    return redirect('login')
            except IntegrityError:
                error = 'IntegrityError'
                return render(request, 'core/registration.html', {'form': form, 'error': error})
        else:
            error = 'WrongEmail'
            return render(request, 'core/registration.html', {'form': form, 'error': error})


class Profile(LoginRequiredMixin, TemplateView):
    template_name = 'core/profile.html'
    model = models.Users
    context_object_name = 'profile'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        user_id = self.kwargs.get('user_id')
        user = models.Users.objects.get(
            id=user_id)
        context['authuser'] = self.request.user
        context['user'] = user
        context['tasksnotdone'] = models.Tasks.objects.filter(owners=user, completed=False)
        context['tasksdone'] = models.Tasks.objects.filter(owners=user, completed=True)
        return context


class FindingFriends(LoginRequiredMixin,
                     TemplateView):
    template_name = 'core/find_friends.html'
    model = models.Users
    context_object_name = 'find_friends'

    # Тут спиздил из Search все.
    # Нужно сделать поиск пользователей.
    # Чтобы можно было кинуть заявку в друзья.
    # Еще вкладку друзья в профиле, где их можно удалить.
    # Еще добавить передачу задачи другу.
    # И на последок забыли пароль.
    # По идее это все
    def get_filters(self):
        return filters.Users(self.request.GET)

    def get_queryset(self):
        return self.get_filters().qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        friends = self.request.user.friends.all()
        user_n_friends = models.Users.objects.filter(id=self.request.user.id) | friends
        context['authuser'] = self.request.user
        context['user'] = self.request.user
        context['users'] = self.get_queryset().exclude(id__in=user_n_friends.values_list('id', flat=True))
        context['filters'] = self.get_filters()
        return context


class UserFriends()

# class AddingFriends(View):
#     template_name = 'core/user_friends.html'
#     model = models.Users
#     context_object_name = 'friends'
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data()
#         context['user'] = self.request.user
#         context['creator'] = self.request.user
#         context['tasks'] = models.Tasks.objects.filter(completed=False)
#         context['tasksdone'] = models.Tasks.objects.filter(completed=True)
#         return context
# Как то сделать отправку запроса в друзья. Как то сделать чтобы вышел запрос у чела. Он подтверждает. Тогда уже они становятся друзьями
# Уведомление вот это все еще сделать как та..


class Calendar(LoginRequiredMixin,
               TemplateView):
    template_name = 'core/calendar.html'
    model = models.Users

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['authuser'] = self.request.user
        context['user'] = self.request.user
        return context


class Pomodoro(LoginRequiredMixin,
               TemplateView):
    template_name = 'core/pomodoro.html'
    model = models.Users

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['authuser'] = self.request.user
        context['user'] = self.request.user
        return context
