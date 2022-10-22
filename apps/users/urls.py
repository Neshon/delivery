from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('sign-in/', auth_views.LoginView.as_view(template_name='sign_in.html')),
    path('sign-out/', auth_views.LogoutView.as_view(next_page='')),
    path('sign-up/', views.sign_up),
    path('accounts/', include('allauth.urls')),


    path('courier/', views.courier_page),

    path('customer/', views.customer_page),
    path('customer/profile/', views.customer_profile, name='profile'),
    path('customer/create_job/', views.create_job_page, name='create_job'),
    path('customer/jobs/current/', views.current_jobs_page, name='current_jobs'),
    path('customer/jobs/archived/', views.archived_jobs_page, name='archived_jobs'),
    path('customer/jobs/<job_id>/', views.job_page, name='job'),
]
