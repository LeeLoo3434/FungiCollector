from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Fungi, FungiNote
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse

# Create your views here.
def home(request):
    return render(request,'home.html')

class FungiList(ListView):
    model = Fungi

class FungiCreate(LoginRequiredMixin, CreateView):
    model = Fungi
    fields = ['name', 'description', 'preferred_environment',
            'edibility', 'date_collected']
    success_url = '/fungi/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class FungiUpdate(LoginRequiredMixin, UpdateView):
    model = Fungi
    fields = ['name', 'description', 'preferred_environment',
            'edibility', 'date_collected']

class FungiDelete(LoginRequiredMixin, DeleteView):
    model = Fungi
    success_url = '/fungi'

def about(request):
    return render(request, 'about.html') 

class FungiDetail(DetailView):
    model = Fungi

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['note'] = self.object.funginote_set.all()
        return context

class FungiNoteCreate(LoginRequiredMixin, CreateView):
    model = FungiNote
    fields = ['note']

    def form_valid(self, form):
        form.instance.fungi = Fungi.objects.get(id=self.kwargs['fungi_id'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('fungi_detail', kwargs={'pk': self.kwargs['fungi_id']})
    
def signup(request):
    error_message = ''
    form = UserCreationForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
        else:
            error_message = 'Invalid sign up - try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)


