from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views, apis

urlpatterns = [
    path('signin/', auth_views.LoginView.as_view(template_name='signin.html')),
    path('signout/', auth_views.LogoutView.as_view(next_page='')),
    path('signup/', views.signup),
    path('accounts/', include('allauth.urls')),

    path('courier/', views.courier_page, name='home'),
    path('courier/jobs/available/', views.available_jobs_page,
         name='available_jobs'),
    path('courier/jobs/available/<id>/', views.available_job_page,
         name='available_job'),
    path('courier/jobs/current/', views.current_job_page,
         name='current_job'),
    path('courier/jobs/current/<id>/take_photo/',
         views.current_job_take_photo_page,
         name='current_job_take_photo_page'),
    path('courier/complete/',
         views.job_complete_page,
         name='job_complete'),
    path('courier/jobs/archived/',
         views.jobs_archived_page,
         name='jobs_archived'),
    path('courier/profile/',
         views.courier_profile,
         name='courier_profile'),

    path('courier/api/jobs/available/', apis.available_jobs_api,
         name='available_jobs_api'),
    path('courier/api/current/<id>/update/', apis.current_job_update_api,
         name='current_job_update_api'),

    path('customer/', views.customer_page, name='home'),
    path('customer/profile/', views.customer_profile, name='profile'),
    path('customer/create_job/', views.create_job_page, name='create_job'),
    path('customer/jobs/current/', views.current_jobs_page, name='current_jobs'),
    path('customer/jobs/archived/', views.archived_jobs_page, name='archived_jobs'),
    path('customer/jobs/<job_id>/', views.job_page, name='job'),
]
