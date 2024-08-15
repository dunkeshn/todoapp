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
        context['username'] = self.request.user.username
        return context


class Tasks(LoginRequiredMixin,
            ListView):
    template_name = 'core/tasks.html'
    model = models.Tasks
    context_object_name = 'tasks'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['username'] = self.request.user.username
        context['tasks'] = models.Tasks.objects.filter(completed=False)
        context['tasksdone'] = models.Tasks.objects.filter(completed=True)
        return context


class AddingTask(View):
    def post(self, request):
        title = request.POST['title']
        if title:
            task = models.Tasks(title=title)
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
        context = {'task': task, 'users': users}
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
        context['username'] = self.request.user.username
        context['tasks'] = self.get_queryset().filter(completed=False)
        context['tasksdone'] = self.get_queryset().filter(completed=True)
        context['filters'] = self.get_filters()
        return context


class Login(FormView):
    template_name = 'core/login_formi.html'
    form_class = forms.LoginForm
    success_url = 'tasks'

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
                return redirect('login')
        return render(request, 'core/login_formi.html', {'form': form})

    # template_name = 'core/login_formi.html'
    # model = models.Users
    #
    # def dispatch(self, request, *args, **kwargs):
    #     if request.user.is_authenticated:
    #         return redirect('home')
    #     return super().dispatch(request, *args, **kwargs)
    #
    # def post(self, request):
    #     email = request.POST.get('login')
    #     password = request.POST.get('password')
    #
    #     usr = authenticate(request,
    #                        username=email,
    #                        password=password)
    #     if usr is not None:
    #         login(request,
    #               usr)
    #         return redirect('tasks')
    #     else:
    #         return redirect('login')


class Logout(TemplateView):
    def get(self, request):
        logout(request)
        return redirect('login')


class Registration(TemplateView):
    template_name = 'core/registration.html'
    model = models.Users

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request,
                                *args,
                                **kwargs)

    def post(self, request):
        first_name = request.POST.get('first_name')
        second_name = request.POST.get('second_name')
        email = request.POST.get('email')
        nick = request.POST.get('nick')
        date_of_birth = request.POST.get('date_of_birth')
        password = request.POST.get('password')
        submit_password = request.POST.get('submit_password')
        if password == submit_password:

            Users.objects.create_user(username=nick,
                                      password=password,
                                      first_name=first_name,
                                      last_name=second_name,
                                      email=email,
                                      date_of_birth=date_of_birth)

            usr = authenticate(request,
                               username=email,
                               password=password)
            if usr is not None:
                login(request,
                      usr)
                return redirect('tasks')
            else:
                return redirect('login')


class Profile(TemplateView):
    template_name = 'core/profile.html'
    model = models.Users
    context_object_name = 'tasks'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['username'] = self.request.user.username
        context['user'] = self.request.user
        context['tasks'] = models.Tasks.objects.all()
        return context


class Calendar(LoginRequiredMixin,
               TemplateView):
    template_name = 'core/calendar.html'
    model = models.Users

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['username'] = self.request.user.username
        return context


class Pomodoro(LoginRequiredMixin,
               TemplateView):
    template_name = 'core/pomodoro.html'
    model = models.Users

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['username'] = self.request.user.username
        return context
