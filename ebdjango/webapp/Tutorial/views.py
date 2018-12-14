from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.generic import View, TemplateView
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .models import *
from .forms import *

# Create your views here.
def HomeView(request):
    return render(request, 'home.html')

def LoginView(request):
    next = request.GET.get('next')
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        if next:
            return redirect(next)
        return redirect('/')

    context = {
        'form': form,
    }
    return render(request, "login.html", context)

def LogoutView(request):
    logout(request)
    return redirect('/')

class UserFormView(View):
    form_class = UserForm
    template_name = 'register.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('Tutorial:home')
        return render(request, self.template_name, {'form': form})

def ForumView(request):
    user = request.user
    ForumPosts =  ForumPost.objects.all()
    #print(ForumPosts)
    context = {'posts': ForumPosts, 'user': user,}
    return render(request, 'ForumPost.html', context)

def ForumPostFormView(request):
    if request.user.is_anonymous:
        messages.info(request, "You must be logged in to make a post!")
        return redirect('Tutorial:login')
    form = ForumPostForm(request.POST or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.user = request.user
        post.save()
        return redirect('Tutorial:forum')
    context = {'form': form, 'title': 'New Post',}
    return render(request, "NewForumPost.html", context)

def ForumPostDeleteView(request, postid):
    post = ForumPost.objects.get(pk = postid)
    post.delete()
    return redirect('/forum/')

def ProfileView(request):
    user = request.user
    context = {'user': user}
    return render(request, "profile.html", context)