# from urllib import request
from typing import Any
from django.http import HttpResponseRedirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Task

# auth
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView

from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth import logout


class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasks')
    
class CustomLogoutView(LoginRequiredMixin, LogoutView):
    def logout_view(request):
        logout(request)
        return HttpResponseRedirect(reverse_lazy('login'))

    def get_success_url(self):
        return reverse_lazy('login')
    # HttpResponseRedirect(self.get_success_url())



class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        print("self.request.user was a class type, I str() it: ", str(self.request.user))
        if(str(self.request.user) != 'cavemankt'):
            context['tasks'] = context['tasks'].filter(user=self.request.user)
        if(str(self.request.user) == 'cavemankt'):
            context['tasks'] = context['tasks']
        context['count'] = context['tasks'].filter(complete=False).count()
        context['admin'] = 'cavemankt'
        print(type(context['admin']))
        return context

class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'taskName'
    template_name = 'base/task.html'
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        return context

class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = {"title", "description", "complete"}
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)

class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = '__all__'
    success_url = reverse_lazy('tasks')

class DeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')
