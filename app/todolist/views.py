from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.urls import reverse
from django.utils import timezone
from .forms import SignUpForm, LoginForm
from .models import CustomUser, Category, Task
from django.contrib.auth.decorators import login_required, user_passes_test

def is_admin(user):
    return user.is_superuser

admin_required = user_passes_test(lambda user: user.is_superuser)

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('category_list')
    else:
        form = SignUpForm()
    return render(request, 'todolist/signup.html', {'form':form})

def login_view(request):
    form = LoginForm(data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('category_list')
            
    return render(request, 'todolist/login.html', {'form':form})

@login_required
def user_tasks_list(request):
    tasks = request.user.tasks.all()
    return render(request, 'todolist/user_tasks_list.html', {'tasks': tasks})

@login_required
@admin_required
def delete_task(request, task_id):
    if request.method == 'POST':
        task = Task.objects.get(id=task_id)
        task.delete()
    return redirect(reverse('category_list'))

@login_required
@admin_required
def create_task(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        category_id = request.POST.get('category')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        priority = request.POST.get('priority')
        description = request.POST.get('description')
        location = request.POST.get('location')
        organizer = request.POST.get('organizer')
        assigned_to_id = request.POST.get('assigned_to')
        category = Category.objects.get(pk=category_id)
        task = Task.objects.create(
            name=name,
            category=category,
            start_date=start_date,
            end_date=end_date,
            priority=priority,
            description=description,
            location=location,
            organizer=organizer,
            assigned_to_id=int(assigned_to_id)
        )

        return redirect('category_list')
    else:
        categories = Category.objects.all()
        users = CustomUser.objects.all()
        return  render(request, 'todolist/create_task.html', {'categories': categories, 'users': users})
    
@login_required
@admin_required
def update_task(request, task_id):
    task = Task.objects.get(pk=task_id)
    if request.method == 'POST':
        if request.method == 'POST':
            task.name = request.POST.get('name')
            task.start_date = request.POST.get('start_date')
            task.end_date = request.POST.get('end_date')
            task.priority = request.POST.get('priority')
            task.description = request.POST.get('description')
            task.location = request.POST.get('location')
            task.organizer = request.POST.get('organizer')
            task.assigned_to_id = request.POST.get('assigned_to')
            task.save()
            return redirect('category_list')
        else:
            return render(request, 'todolist/update_task.html', {'task':task})
        
@login_required
@admin_required
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'todolist/category_list.html', {'categories': categories})

@login_required
@admin_required
def create_category(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        Category.objects.create(name=name)
        return redirect('category_list')
    return render(request, 'todolist/create_category.html')

@login_required
@admin_required
def delete_category(request, category_id):
    category = Category.objects.get(pk=category_id)
    if category.task_set.exists():
        messages.error(
            request, "Вы не можете удалить категорию, содержащую задачи.")
    else:
        category.delete()
        messages.success(request, "Категория успешно удалена.")
    return redirect('category_list')

@login_required
@admin_required
def category_tasks(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    tasks = category.task_set.all()
    return render(request, 'todolist/category_tasks.html', {'category': category, 'tasks': tasks})

@login_required
@admin_required
def task_chart(request):
    categories = Category.objects.all()
    pending_counts = {}
    for category in categories:
        pending_counts[category.name] = Task.objects.filter(
            category=category,
            start_date__gt=timezone.now()
        ).count()
    return render(request, 'todolist/task_chart.html', {'pending_counts': pending_counts})