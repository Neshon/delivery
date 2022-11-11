from django.urls import path, include
from django.contrib.auth import views as auth_views

from . import views


urlpatterns = [
    path('signin/', auth_views.LoginView.as_view(template_name='signin.html')),
    path('signout/', auth_views.LogoutView.as_view(next_page='')),
    path('signup/', views.signup),
    path('accounts/', include('allauth.urls')),
]
