from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from .forms import TasksForm
from .models import Tasks
from django.utils import timezone
from django.contrib.auth.decorators import login_required
# Create your views here.


def home(request):
    return render(request, 'home.html')


def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {'form': UserCreationForm})
    else:
        if request.POST['password1'] == request.POST['password2']:
            # registrar usuario
            try:
                user = User.objects.create_user(
                    username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request,user)
                return redirect(tasks)
            except:
                return render(request, 'signup.html', {'form': UserCreationForm, 'error': 'el usuario ya existe'})
        return render(request, 'signup.html', {'form': UserCreationForm, 'error': 'el password no coicide'})

@login_required
def tasks(request):
    tareas = Tasks.objects.filter(usuario =  request.user,dia_completado__isnull=True )
    return render(request, 'tasks.html',{'Tareas':tareas})

@login_required
def tasks_completed(request):
    tareas = Tasks.objects.filter(usuario =  request.user,dia_completado__isnull=False ).order_by('-dia_completado')
    return render(request, 'completadas.html',{'Tareas':tareas})

@login_required    
def create_tasks(request):
    if request.method == 'GET':
        return render(request,'create_tasks.html',{'form':TasksForm})
    else:
        form = TasksForm(request.POST)
        newTask = form.save(commit= False)
        newTask.usuario_id = request.user.id
        
        newTask.save()
        return redirect(tasks)

@login_required
def task_detail(request, task_id):
    if request.method == 'GET':
        tarea = get_object_or_404(Tasks, pk = task_id, usuario = request.user)
        formulario = TasksForm(instance= tarea)
        return render(request,'tarea_detalle.html',{'tarea':tarea,'formulario':formulario} )
    else:
        try:
            tarea = get_object_or_404(Tasks, pk=task_id, usuario = request.user)
            formulario = TasksForm(request.POST, instance=tarea)
            formulario.save()
            return redirect('tasks')
        except ValueError:
            return render(request,'tarea_detalle.html',{'tarea':tarea,'formulario':formulario, 'error':'Error al actualizar'} )

@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Tasks, pk=task_id, usuario = request.user)
    if request.method == 'POST':
        task.dia_completado = timezone.now()
        task.save() 
        return redirect('tasks')

login_required
def delete_task(request, task_id):
    task = get_object_or_404(Tasks, pk=task_id, usuario = request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')        

@login_required        
def signout(request):
    logout(request)
    return redirect(home)


def signin(request):
    if request.method == 'GET':
        return render(request,'signin.html',{'form':AuthenticationForm})
    else:
        user = authenticate(request,username = request.POST['username'], password = request.POST['password'])
        if user is None:
            return render(request,'signin.html',{'form':AuthenticationForm, 'error':'usuario o contraseña invalido'})
        else:
            login(request,user)
            return redirect(tasks)
        