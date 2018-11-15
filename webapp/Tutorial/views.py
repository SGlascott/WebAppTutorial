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

def registerView(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserForm()
    return render(request, 'signup.html', {'form': form})

def ForumView(request):
    user = request.user
    ForumPosts =  ForumPost.objects.all()
    #print(ForumPosts)
    context = {'posts': ForumPosts, 'user': user,}
    return render(request, 'ForumPost.html', context)

def ForumPostFormView(request):
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
