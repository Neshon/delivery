from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from .models import Job


@csrf_exempt
@login_required(login_url='/users/signin/?next=/users/courier/')
def available_jobs_api(request):
    jobs = list(Job.objects.filter(status=Job.PROCESSING_STATUS).values())

    return JsonResponse({
        'success': True,
        'jobs': jobs
    })


@csrf_exempt
@login_required(login_url='/users/signin/?next=/users/courier/')
def current_job_update_api(request, id):
    job = Job.objects.filter(
        id=id,
        courier=request.user.courier,
        status__in=[
            Job.PICKING_STATUS,
            Job.DELIVERING_STATUS
        ]
    ).latest('created_at')

    if job.status == Job.PICKING_STATUS:
        job.pickup_photo = request.FILES['pickup_photo']
        job.picked_up_at = timezone.now()
        job.status = Job.DELIVERING_STATUS
        job.save()

        try:
            layer = get_channel_layer()
            async_to_sync(layer.group_send)('job_' + str(job.id), {
                'type': 'job_update',
                'job': {
                    'status': job.get_status_display(),
                    'pickup_photo': job.pickup_photo.url,
                }
            })
        except:
            pass

    elif job.status == Job.DELIVERING_STATUS:
        job.delivery_photo = request.FILES['delivery_photo']
        job.delivered_at = timezone.now()
        job.status = Job.COMPLETED_STATUS
        job.save()

        try:
            layer = get_channel_layer()
            async_to_sync(layer.group_send)('job_' + str(job.id), {
                'type': 'job_update',
                'job': {
                    'status': job.get_status_display(),
                    'delivery_photo': job.delivery_photo.url,
                }
            })
        except:
            pass

    return JsonResponse({
        'success': True
    })
