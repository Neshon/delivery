from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views, apis


urlpatterns = [
    path('signin/', auth_views.LoginView.as_view(template_name='signin.html')),
    path('signout/', auth_views.LogoutView.as_view(next_page='')),
    path('signup/', views.signup),
    path('accounts/', include('allauth.urls')),

    path('courier/api/jobs/available/', apis.available_jobs_api,
         name='available_jobs_api'),
    path('courier/api/current/<id>/update/', apis.current_job_update_api,
         name='current_job_update_api'),
]
