from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Fungi, Comment
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.urls import reverse

def home(request):
    return render(request,'home.html')


class FungiList(ListView):
    model = Fungi


class FungiCreate(LoginRequiredMixin, CreateView):
    model = Fungi
    fields = ['name', 'description', 'preferred_environment',
            'edibility', 'date_collected', 'identified', 'photo']  # Updated the fields list to include 'identified'
    success_url = '/fungi/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class FungiUpdate(LoginRequiredMixin, UpdateView):
    model = Fungi
    fields = ['name', 'description', 'preferred_environment',
            'edibility', 'date_collected', 'identified', 'photo']

    def get_success_url(self):
        return reverse_lazy('fungi_detail', kwargs={'pk': self.object.pk})



class FungiDelete(LoginRequiredMixin, DeleteView):
    model = Fungi
    success_url = '/fungi/'


def about(request):
    return render(request, 'about.html') 


class FungiDetail(DetailView):
    model = Fungi

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['notes'] = self.object.comment_set.all()
        return context  # Removed the Habitat context since it's not in the models anymore



class CommentCreate(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ['content']

    def form_valid(self, form):
        form.instance.fungi = Fungi.objects.get(id=self.kwargs['fungi_id'])
        form.instance.user = self.request.user
        messages.success(self.request, "Comment created successfully!")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('fungi_detail', kwargs={'pk': self.kwargs['fungi_id']})

class CommentUpdate(LoginRequiredMixin, UpdateView):
    model = Comment
    fields = ['content']

    def get_success_url(self):
        return reverse('fungi_detail', kwargs={'pk': self.object.fungi.id})

class CommentDelete(LoginRequiredMixin, DeleteView):
    model = Comment

    def get_success_url(self):
        return reverse('fungi_detail', kwargs={'pk': self.object.fungi.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fungi'] = self.object.fungi  # Add the related fungi instance to the context
        return context

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, 'Invalid sign up - try again')
    else:
        form = UserCreationForm()

    return render(request, 'registration/signup.html', {'form': form})

