from django.shortcuts import render, redirect
from django.urls import reverse
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth.decorators import login_required


from config.settings import base
from apps.delivery.models import Job


def home(request):
    return render(request, 'home.html')


@login_required(login_url='/users/signin/?next=/courier/')
def courier_page(request):
    return redirect(reverse('courier:available_jobs'))


@login_required(login_url='/users/signin/?next=/courier/')
def available_jobs_page(request):
    return render(request, 'courier/available_jobs.html', {
        'google_map_api_key': base.GOOGLE_MAP_API_KEY,
    })


@login_required(login_url='/users/signin/?next=/courier/')
def available_job_page(request, id):
    job = Job.objects.filter(id=id, status=Job.PROCESSING_STATUS).last()

    if not Job:
        return redirect(reverse('courier:available_jobs'))

    if request.method == 'POST':
        job.courier = request.user.courier
        job.status = Job.PICKING_STATUS
        job.save()

        try:
            layer = get_channel_layer()
            async_to_sync(layer.group_send)('job_' + str(job.id), {
                'type': 'job_update',
                'job': {
                    'status': job.get_status_display(),
                }
            })
        except:
            pass

        return redirect(reverse('courier:current_job'))

    return render(request, 'courier/available_job.html', {
        'job': job,
    })


@login_required(login_url='/users/signin/?next=/courier/')
def current_job_page(request):
    job = Job.objects.filter(courier=request.user.courier,
                             status__in=[
                                 Job.PICKING_STATUS,
                                 Job.DELIVERING_STATUS,
                             ]
                             ).last()

    return render(request, 'courier/current_job.html', {
        'google_map_api_key': base.GOOGLE_MAP_API_KEY,
        'job': job,
    })


@login_required(login_url='/users/signin/?next=/courier/')
def current_job_take_photo_page(request, id):
    job = Job.objects.filter(
        id=id,
        courier=request.user.courier,
        status__in=[
            Job.PICKING_STATUS,
            Job.DELIVERING_STATUS
        ]
    ).last()

    if not job:
        return redirect(reverse('courier:current_job'))

    return render(request, 'courier/current_job_take_photo_page.html', {
        'job': job
    })


@login_required(login_url='/users/signin/?next=/courier/')
def job_complete_page(request):
    return render(request, 'courier/job_complete.html')


@login_required(login_url='/users/signin/?next=/courier/')
def archived_jobs_page(request):
    jobs = Job.objects.filter(
        courier=request.user.courier,
        status=Job.COMPLETED_STATUS
    )

    return render(request, 'courier/archived_jobs.html', {
        'jobs': jobs
    })


@login_required(login_url='/users/signin/?next=/courier/')
def courier_profile(request):
    jobs = Job.objects.filter(
        courier=request.user.courier,
        status=Job.COMPLETED_STATUS
    )

    total_earnings = round(sum(job.price for job in jobs) * 0.8, 2)
    total_jobs = len(jobs)
    total_km = round(sum(job.distance for job in jobs), 2)

    return render(request, 'courier/profile.html', {
        'total_earnings': total_earnings,
        'total_jobs': total_jobs,
        'total_km': total_km
    })
