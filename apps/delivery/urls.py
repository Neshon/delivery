from django.urls import path
from . import apis, views


app_name = 'courier'
urlpatterns = [
    path('', views.courier_page, name='home'),
    path('jobs/available/', views.available_jobs_page,
         name='available_jobs'),
    path('jobs/available/<id>/', views.available_job_page,
         name='available_job'),
    path('jobs/current/', views.current_job_page,
         name='current_job'),
    path('jobs/current/<id>/take_photo/',
         views.current_job_take_photo_page,
         name='current_job_take_photo_page'),
    path('complete/',
         views.job_complete_page,
         name='job_complete'),
    path('jobs/archived/',
         views.archived_jobs_page,
         name='archived_jobs'),
    path('profile/',
         views.courier_profile,
         name='courier_profile'),
    path('api/jobs/available/', apis.available_jobs_api,
         name='available_jobs_api'),
    path('api/current/<id>/update/', apis.current_job_update_api,
         name='current_job_update_api'),
]
