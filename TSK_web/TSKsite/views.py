import json
import datetime
from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required

from .forms import UserRegisterForm, ProfileForm, CreationForm
from .models import Project, Task


def get_bar_context(request):
    menu = []
    if request.user.is_authenticated:
        menu.append(dict(title=str(request.user), url=reverse('profile', kwargs={'stat': 'reading'})))
        menu.append(dict(title='Создать новый проект', url=reverse('project_creation')))
        menu.append(dict(title='Выйти', url=reverse('logout')))
    else:
        pass

    return menu


class UserRegisterView(SuccessMessageMixin, CreateView):
    form_class = UserRegisterForm
    success_url = reverse_lazy('login')
    template_name = 'register.html'
    success_message = 'Вы успешно зарегистрировались. Можете войти на сайт!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регистрация на сайте'

        return context


def logout_view(request):
    logout(request)
    return redirect('index')


def index_page(request):
    context = {
        'bar': get_bar_context(request),
        'user': request.user
    }
    return render(request, 'index.html', context)


@login_required
def profile(request, stat):
    user = request.user

    if user.is_anonymous:
        return redirect('login')

    projects = Project.objects.filter(author=user)

    profile_info = {
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
    }

    if request.method == 'POST':
        form = ProfileForm(request.POST)

        if form.is_valid():
            User.objects.filter(id=user.id).update(username=form.data["username"], email=form.data["email"],
                                                   first_name=form.data["first_name"], last_name=form.data["last_name"])

            return redirect(reverse('profile', kwargs={'stat': 'reading'}))
    else:
        form = ProfileForm(initial={
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
        })

    context = {
        'bar': get_bar_context(request),
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'projects': projects,
        'stat': stat,
        'form': form,
        'profile_info': profile_info,
        'url': reverse('profile', kwargs={'stat': 'editing'}),
        'url_back': reverse('profile', kwargs={'stat': 'reading'})
    }

    return render(request, 'profile.html', context)


@login_required
def project_creation(request):
    if request.method == 'POST':
        form = CreationForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.author = request.user
            project.save()
            return redirect(reverse('project_detail', kwargs={'stat': 'reading', 'project_id': str(project.id)}))
    else:
        form = CreationForm()
        context = {
            'bar': get_bar_context(request),
            'form': form,
        }
        return render(request, 'project_creation.html', context)


@login_required
def project_detail(request, stat, project_id):
    user = request.user
    project = Project.objects.get(id=int(project_id))
    tasks = project.tasks.all()

    if request.method == 'POST' and stat == 'editing':
        form = CreationForm(request.POST)

        if form.is_valid():
            Project.objects.filter(id=project.id).update(name=form.data["name"], description=form.data["description"])

            task_prefixes = [key.split('-')[1] for key in request.POST if 'tasks-' in key]
            for prefix in task_prefixes:
                task_name = request.POST[f'tasks-{prefix}-text']
                task_description = request.POST[f'tasks_description-{prefix}-text']

                new_task = Task.objects.create(
                    name=task_name,
                    description=task_description,
                    author=user,
                    done=False
                )
                project.tasks.add(new_task)

            return redirect(reverse('project_detail', kwargs={'stat': 'reading', 'project_id': str(project.id)}))
    else:
        form = CreationForm(initial={
            'name': project.name,
            'description': project.description,
        })

    context = {
        'bar': get_bar_context(request),
        'project': project,
        'tasks': tasks,
        'stat': stat,
        'form': form
    }
    return render(request, 'project_detail.html', context)


@login_required
def update_task_cond(request, task_id):
    if request.method == 'PATCH':
        try:
            task = Task.objects.get(id=task_id)
            done = json.loads(request.body.decode('utf-8')).get('done')
            task.done = done
            task.save()
            return JsonResponse({'status': 'success', 'message': 'Состояние задачи успешно обновлено'})
        except Task.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Задача не найдена'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Неверный метод запроса'})
