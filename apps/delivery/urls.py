from django.urls import path
from . import apis

urlpatterns = [
    path('courier/api/jobs/available/', apis.available_jobs_api,
         name='available_jobs_api'),
    path('courier/api/current/<id>/update/', apis.current_job_update_api,
         name='current_job_update_api'),
]
