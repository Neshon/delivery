import requests
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

from config import settings
from . import forms
from .models import Job


def home(request):
    return render(request, 'home.html')


# courier
@login_required(login_url='/sign-in/?next=/users/courier/')
def courier_page(request):
    return render(request, 'home.html')


@login_required(login_url='/sign-in/?next=/users/courier/')
def available_jobs_page(request):
    return render(request, 'courier/available_jobs.html', {
        'google_map_api_key': settings.GOOGLE_MAP_API_KEY,
    })


@login_required(login_url='/sign-in/?next=/users/courier/')
def available_job_page(request, id):
    job = Job.objects.filter(id=id, status=Job.PROCESSING_STATUS).last()

    if not Job:
        return redirect(reverse('available_jobs'))

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

        return redirect(reverse('current_job'))

    return render(request, 'courier/available_job.html', {
        'job': job,
    })


@login_required(login_url='/sign-in/?next=/users/courier/')
def current_job_page(request):
    job = Job.objects.filter(courier=request.user.courier,
                             status__in=[
                                 Job.PICKING_STATUS,
                                 Job.DELIVERING_STATUS,
                             ]
                             ).last()

    return render(request, 'courier/current_job.html', {
        'google_map_api_key': settings.GOOGLE_MAP_API_KEY,
        'job': job,
    })


@login_required(login_url='/sign-in/?next=/users/courier/')
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
        return redirect(reverse('current_job'))

    return render(request, 'courier/current_job_take_photo_page.html', {
        'job': job
    })


@login_required(login_url='/sign-in/?next=/users/courier/')
def job_complete_page(request):
    return render(request, 'courier/job_complete.html')


@login_required(login_url='/sign-in/?next=/users/courier/')
def jobs_archived_page(request):
    jobs = Job.objects.filter(
        courier=request.user.courier,
        status=Job.COMPLETED_STATUS
    )

    return render(request, 'courier/jobs_archived.html', {
        'jobs': jobs
    })


@login_required(login_url='/sign-in/?next=/users/courier/')
def courier_profile(request):
    jobs = Job.objects.filter(
        courier=request.user.courier,
        status=Job.COMPLETED_STATUS
    )

    total_earnings = round(sum(job.price for job in jobs) * 0.8, 2)
    total_jobs = len(jobs)
    total_km = sum(job.distance for job in jobs)

    return render(request, 'courier/profile.html', {
        'total_earnings': total_earnings,
        'total_jobs': total_jobs,
        'total_km': total_km
    })


# customer
@login_required(login_url='/sign-in/?next=/users/customer/')
def customer_page(request):
    return redirect(reverse('profile'))


@login_required(login_url='/sign-in/?next=/users/customer/')
def customer_profile(request):
    user_form = forms.BasicUserForm(instance=request.user)
    customer_form = forms.BasicCustomerForm(instance=request.user.customer)
    password_form = PasswordChangeForm(request.user)

    if request.method == 'POST':
        if request.POST.get('action') == 'update_profile':
            user_form = forms.BasicUserForm(request.POST,
                                            instance=request.user)
            customer_form = forms.BasicCustomerForm(request.POST,
                                                    request.FILES,
                                                    instance=request.user.customer)

            if user_form.is_valid() and customer_form.is_valid():
                user_form.save()
                customer_form.save()

                messages.success(request, "You profile has been updated")
                return redirect(reverse('profile'))

        if request.POST.get('action') == 'update_password':
            password_form = PasswordChangeForm(request.user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)

                messages.success(request, "You password has been updated")
                return redirect(reverse('profile'))

    return render(request, 'customer/profile.html',
                  {
                      'user_form': user_form,
                      'customer_form': customer_form,
                      'password_form': password_form
                  })


@login_required(login_url='/sign-in/?next=/users/customer/')
def create_job_page(request):
    current_customer = request.user.customer
    has_current_job = Job.objects.filter(customer=current_customer,
                                         status__in=[
                                             Job.PROCESSING_STATUS,
                                             Job.PICKING_STATUS,
                                             Job.DELIVERING_STATUS
                                         ]).exists()

    if has_current_job:
        messages.warning(request, "You currently have a processing job.")
        return redirect(reverse('current_jobs'))
    creating_job = Job.objects.filter(customer=current_customer,
                                      status=Job.CREATING_STATUS).last()

    step1_form = forms.JobCreateStep1Form(instance=creating_job)
    step2_form = forms.JobCreateStep2Form(instance=creating_job)
    step3_form = forms.JobCreateStep3Form(instance=creating_job)

    if request.method == 'POST':
        if request.POST.get('step') == '1':
            step1_form = forms.JobCreateStep1Form(request.POST,
                                                  request.FILES,
                                                  instance=creating_job)
            if step1_form.is_valid():
                creating_job = step1_form.save(commit=False)
                creating_job.customer = current_customer
                creating_job.save()

                messages.success(request, "You job has been created")
                return redirect(reverse('create_job'))

        elif request.POST.get('step') == '2':
            step2_form = forms.JobCreateStep2Form(request.POST,
                                                  instance=creating_job)
            if step2_form.is_valid():
                creating_job = step2_form.save()

                messages.success(request, "You pickup has been created")
                return redirect(reverse('create_job'))

        elif request.POST.get('step') == '3':
            step3_form = forms.JobCreateStep3Form(request.POST,
                                                  instance=creating_job)
            if step3_form.is_valid():
                creating_job = step3_form.save()
                try:
                    r = requests.get(
                        f"https://maps.googleapis.com/maps/api/distancematrix/"
                        f"json?origins={creating_job.pickup_address}"
                        f"&destinations={creating_job.delivery_address}"
                        f"&key={settings.GOOGLE_MAP_API_KEY}")

                    # print(r.json()['rows'])
                    distance = r.json()['rows'][0]['elements'][0]['distance']['value']
                    duration = r.json()['rows'][0]['elements'][0]['duration']['value']
                    creating_job.distance = round(distance / 1000, 2)
                    creating_job.duration = int(duration / 60)
                    creating_job.price = creating_job.distance * 5
                    creating_job.save()
                except Exception as e:
                    print(e)
                    messages.error(request, "Error in google api")
                creating_job.status = Job.PROCESSING_STATUS
                creating_job.save()
                messages.success(request, "You delivery has been created")
                return redirect(reverse('create_job'))

    if not creating_job:
        current_step = 1
    elif creating_job.pickup_name:
        current_step = 3
    else:
        current_step = 2

    return render(request, 'customer/create_job.html', {
        'google_map_api_key': settings.GOOGLE_MAP_API_KEY,
        'job': creating_job,
        'step': current_step,
        'step1_form': step1_form,
        'step2_form': step2_form,
        'step3_form': step3_form,
    })


@login_required(login_url='/sign-in/?next=/users/customer/')
def current_jobs_page(request):
    jobs = Job.objects.filter(customer=request.user.customer,
                              status__in=[
                                  Job.PROCESSING_STATUS,
                                  Job.PICKING_STATUS,
                                  Job.DELIVERING_STATUS
                              ])
    return render(request, 'customer/jobs.html', {
        'jobs': jobs
    })


@login_required(login_url='/sign-in/?next=/users/customer/')
def job_page(request, job_id):
    job = Job.objects.get(id=job_id)

    if request.method == 'POST' and job.status == Job.PROCESSING_STATUS:
        job.status = Job.CANCELED_STATUS
        job.save()
        return redirect(reverse('archived_jobs'))

    return render(request, 'customer/job.html', {
        'google_map_api_key': settings.GOOGLE_MAP_API_KEY,
        'job': job
    })


@login_required(login_url='/sign-in/?next=/users/customer/')
def archived_jobs_page(request):
    jobs = Job.objects.filter(customer=request.user.customer,
                              status__in=[
                                  Job.COMPLETED_STATUS,
                                  Job.CANCELED_STATUS,
                              ])
    return render(request, 'customer/jobs.html', {
        'jobs': jobs
    })


def sign_up(request):
    form = forms.SignUpForm()
    if request.method == 'POST':
        form = forms.SignUpForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email').lower()
            user = form.save(commit=False)
            user.username = email
            user.save()

            login(request, user,
                  backend='django.contrib.auth.backends.ModelBackend')
            return redirect('/')
    return render(request, 'sign_up.html', {'form': form})
