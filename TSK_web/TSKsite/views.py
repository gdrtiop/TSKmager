# views.py
import json
import datetime
from django.contrib.auth.models import User
from django.http import Http404, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.views import generic
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required

from .forms import UserRegisterForm, ProfileForm, CreationForm, AddUserForm, TaskForm, ComplaintForm, AnswerComplaintForm
from .models import Project, Task, Complaint


def get_bar_context(request):
    menu = []
    if request.user.is_authenticated:
        menu.append(dict(title=str(request.user), url=reverse('profile', kwargs={'stat': 'reading'})))
        menu.append(dict(title='Создать новый проект', url=reverse('project_creation')))
        menu.append(dict(title='Обратная связь', url=reverse('complaints')))
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
    messages.success(request, 'Вы успешно вышли из системы.')
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
    projects_as_member = Project.objects.filter(members=user)

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
            messages.success(request, 'Профиль успешно обновлен.')
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
        'projects_as_members': projects_as_member,
        'projects': projects,
        'stat': stat,
        'form': form,
        'profile_info': profile_info,
        'url': reverse('profile', kwargs={'stat': 'editing'}),
        'url_back': redirect(reverse('profile', kwargs={'stat': 'reading'}))
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
            messages.success(request, 'Проект успешно создан.')
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
    context = {}

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

            messages.success(request, 'Проект успешно обновлен!')
            return redirect(reverse('project_detail', kwargs={'stat': 'reading', 'project_id': str(project.id)}))
    else:
        form = CreationForm(initial={
            'name': project.name,
            'description': project.description,
        })

    if request.method == 'POST' and stat == 'reading':
        form_add = AddUserForm(request.POST)

        if form_add.is_valid():
            new_memb = form_add.data['new_memb']
            try:
                new_user = User.objects.get(username=new_memb)
                Project.objects.get(id=project.id).members.add(new_user)
                messages.success(request, 'Пользователь успешно добавлен к проекту!')
            except User.DoesNotExist:
                messages.error(request, 'Пользователь с таким именем не найден.')

    else:
        pass

    form_add = AddUserForm()
    tasks = project.tasks.all()
    tasks_form = []
    for task in tasks:
        tasks_form.append(TaskForm(initial={'name': task.name, 'description': task.description}))

    context = {
        'bar': get_bar_context(request),
        'project': project,
        'tasks': tasks,
        'stat': stat,
        'form': form,
        'form_add': form_add,
        'tasks_form': tasks_form,
    }
    return render(request, 'project_detail.html', context)


@login_required
def update_task_cond(request, task_id):
    if request.method == 'PATCH':
        try:
            task = Task.objects.get(id=task_id)
            done = json.loads(request.body.decode('utf-8')).get('done')
            task.done = done
            if done:
                task.who_done = request.user
            else:
                task.who_done = None
            task.save()

            response_data = {
                'status': 'success',
                'message': 'Состояние задачи успешно обновлено',
                'done': task.done,
                'who_done': task.who_done.username if task.who_done else None
            }
            return JsonResponse(response_data)
        except Task.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Задача не найдена'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Неверный метод запроса'})


@login_required()
def complaints(request):
    if request.user.is_superuser:
        status = 1
        data = Complaint.objects.filter().order_by('data')
    else:
        status = 0
        data = Complaint.objects.filter(author=request.user)

    data = list(reversed(data))

    context = {
        'bar': get_bar_context(request),
        'data': data,
        'status': status
    }

    return render(request, 'complaints.html', context)


@login_required()
def create_complaint(request):

    if request.method == 'POST':
        form = ComplaintForm(request.POST)

        if form.is_valid():
            saver_form = Complaint(text=form.data['text'], author=request.user, data=datetime.datetime.now(), answer='')
            saver_form.save()

            context = {
                'bar': get_bar_context(request),
                'form': form,
                'text': form.data['text']
            }
            messages.success(request, 'Жалоба успешно создана.')
            return redirect(reverse('complaints'))
    else:
        form = ComplaintForm

        context = {
            'bar': get_bar_context(request),
            'form': form
        }

    return render(request, 'create_complaint.html', context)


@login_required()
def complaint_answer(request, complaint_id):

    complaint = Complaint.objects.get(id=complaint_id)

    if request.method == 'POST':
        answer_form = AnswerComplaintForm(request.POST)

        if answer_form.is_valid():
            complaint.answer = answer_form.data.get('answer')
            complaint.save()
            messages.success(request, 'Ответ на жалобу успешно отправлен.')
            return redirect(reverse('complaints'))
    else:
        answer_form = AnswerComplaintForm(initial={
            'answer': complaint.answer,
        })

    context = {
        'bar': get_bar_context(request),
        'form': answer_form,
        'complaint': complaint,
        'url': reverse('complaint_answer', args=(complaint_id,))
    }

    return render(request, 'complaint_answer.html', context)
