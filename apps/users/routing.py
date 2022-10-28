from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path("ws/jobs/<job_id>/", consumers.JobConsumer.as_asgi()),
]
