from django.urls import path
from . import views


app_name = 'customer'
urlpatterns = [
    path('', views.customer_page, name='home'),
    path('profile/', views.customer_profile, name='profile'),
    path('create_job/', views.create_job_page, name='create_job'),
    path('jobs/current/', views.current_jobs_page, name='current_jobs'),
    path('jobs/archived/', views.archived_jobs_page, name='archived_jobs'),
    path('jobs/<job_id>/', views.job_page, name='job'),
]
