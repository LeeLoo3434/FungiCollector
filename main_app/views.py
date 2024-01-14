from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Fungi, Comment
from userprofile.models import UserProfile, Like  # <-- Adjusted import
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect
from .forms import UserProfileForm
from django.contrib.auth.models import User

def home(request):
    return render(request,'home.html')


class FungiList(ListView):
    model = Fungi


class FungiCreate(LoginRequiredMixin, CreateView):
    model = Fungi
    fields = ['name', 'description', 'preferred_environment',
            'edibility', 'date_collected', 'identified', 'photo','is_public']  # Updated the fields list to include 'identified'
    success_url = '/fungi/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class FungiUpdate(LoginRequiredMixin, UpdateView):
    model = Fungi
    fields = ['name', 'description', 'preferred_environment',
            'edibility', 'date_collected', 'identified', 'photo','is_public']

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

    def get(self, request, *args, **kwargs):
        fungi = Fungi.objects.get(id=self.kwargs['fungi_id'])
        if not fungi.is_public:
            messages.error(self.request, "You cannot comment on a private post!")
            return HttpResponseRedirect(reverse('fungi_detail', kwargs={'pk': fungi.id}))
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        fungi = Fungi.objects.get(id=self.kwargs['fungi_id'])
        if not fungi.is_public:
            messages.error(self.request, "You cannot comment on a private post!")
            return HttpResponseRedirect(reverse('fungi_detail', kwargs={'pk': fungi.id}))
        return super().post(request, *args, **kwargs)

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
    
def profile_page(request, user_id):
    user = User.objects.get(pk=user_id)
    user_profile, created = UserProfile.objects.get_or_create(user=user)

    # Fetch the list of fungi associated with this user
    fungi_list = Fungi.objects.filter(user=user)  # Adjust the filter according to your model relationships

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('profile_page', user_id=user.id)
    else:
        form = UserProfileForm(instance=user_profile)

    context = {
        'user_profile': user_profile,
        'profile_form': form,
        'fungi_list': fungi_list  # Add the fungi list to the context
    }
    return render(request, 'profile_page.html', context)

class UserFeed(ListView):
    model = Fungi
    template_name = 'public_feed.html'

    def get_queryset(self):
        return Fungi.objects.filter(is_public=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        try:
            user_profile = UserProfile.objects.get(user=self.request.user)
        except UserProfile.DoesNotExist:
            user_profile = None

        # Add a dictionary to the context indicating which posts the user can interact with
        # This is based on whether the user and the post's user are friends
        can_interact = {}
        for fungi in context['fungi_list']:
            try:
                fungi_owner_profile = UserProfile.objects.get(user=fungi.user)
                can_interact[fungi.id] = user_profile.are_friends(fungi_owner_profile) if user_profile else False
            except UserProfile.DoesNotExist:
                can_interact[fungi.id] = False
        
        context['can_interact'] = can_interact
        return context
        

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile_page', user_id=user.id)  # Redirecting to the profile_page
        else:
            messages.error(request, 'Invalid sign up - try again')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


# Other imports and views...

@login_required
@require_POST
def like_fungi(request, fungi_id):
    fungi_id = request.POST.get('id')
    fungi = Fungi.objects.get(id=fungi_id)

    # Toggle like status
    if request.user in fungi.liked_by.all():
        fungi.liked_by.remove(request.user)
        liked = False
    else:
        fungi.liked_by.add(request.user)
        liked = True

    fungi.likes = fungi.liked_by.count()  # Update like count
    fungi.save()

    return JsonResponse({'liked': liked, 'total_likes': fungi.likes})

