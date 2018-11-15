from django.urls import path, include
from .views import *

app_name = 'Tutorial'
urlpatterns = [
    path('', HomeView, name = 'home'),
    path('login/', LoginView, name = 'login'),
    path('logout/', LogoutView, name = 'logout'),
    path('register/', registerView, name='register'),
    path('forum/',ForumView,name='forum'),
    path('forum/new/', ForumPostFormView, name = 'newForum'),
    path('forum/delete/<postid>/', ForumPostDeleteView, name = 'deleteForum'),
]