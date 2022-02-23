from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm  # Creates user when submitted
from django.contrib.auth.mixins import LoginRequiredMixin  # Can require different roles like: admin
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic.list import ListView

from .forms import LoginForm
from .models import Task, Profile


def login_view(request):
    form = LoginForm(request.POST or None)

    if request.POST.get('beta_key') != None:  # If beta key is entered
        if Profile.objects.filter(login_code=request.POST.get('beta_key')).exists():
            beta_key = request.POST.get('beta_key')  # Get the beta key from the form
            user = User.objects.get(profile__login_code=beta_key)  # Get the user with the beta key
            login(request, user)  # Log the user in
            return redirect("tasks")  # Redirect because the login was a success
    if request.POST and form.is_valid():
        if user := form.login(request):  # Same thing as saying if user when user equals form.login(request)
            login(request, user)
            return redirect("tasks")  # Redirect because the login was a success
    context = {
        'form': form
    }
    return render(request, 'core/login.html', context)


class RegisterPage(FormView):
    template_name = 'core/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')  # Redirects to the task_list.html by its name

    # If the form is valid, save the user and login the user automatically
    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    # If the user is logged and tries to access the register page, redirect to the task_list.html
    # This explains *args, **kwargs - https://stackoverflow.com/questions/13977624/args-and-kwargs-in-django-views#:~:text=*args%20and%20**kwargs%20are%20used%20to%20pass%20a%20variable,and%20double%20for%20keyworded%20argument.
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterPage, self).get(*args, **kwargs)


class TaskList(LoginRequiredMixin, ListView):  # ListView returns a template with a list of objects
    model = Task
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Makes sure user only gets their own data with: filter(user=self.request.user)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()

        search_input = self.request.GET.get('search-area') or ''  # or '' in case the search is blank
        if search_input:
            context['tasks'] = context['tasks'].filter(
                title__startswith=search_input)

        context['search_input'] = search_input
        return context


class TaskDetail(LoginRequiredMixin, DetailView):  # Add LoginRequiredMixin before Views like: DetailView
    model = Task
    context_object_name = 'task'
    template_name = 'core/task.html'


class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'description', 'complete']  # Or can list all model fields like: __all__
    success_url = reverse_lazy('tasks')  # Redirects to the task_lsit.html by its name

    # Overrides the default form_valid method to add the user to the form as the task author
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)


class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('tasks')  # If we are using success_url we have to use reverse_lazy().
    # If we are reversing inside a function we can use reverse().


class DeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')
