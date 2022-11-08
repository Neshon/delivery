import requests

from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

from apps.customer import forms
from config.settings import base

from apps.users.models import Job


@login_required(login_url='/users/signin/?next=/customer/')
def customer_page(request):
    return redirect(reverse('customer:current_jobs'))


@login_required(login_url='/users/signin/?next=/customer/')
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
                return redirect(reverse('customer:profile'))

        if request.POST.get('action') == 'update_password':
            password_form = PasswordChangeForm(request.user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)

                messages.success(request, "You password has been updated")
                return redirect(reverse('customer:profile'))

    return render(request, 'customer/profile.html',
                  {
                      'user_form': user_form,
                      'customer_form': customer_form,
                      'password_form': password_form
                  })


@login_required(login_url='/users/signin/?next=/customer/')
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
        return redirect(reverse('customer:current_jobs'))
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

                return redirect(reverse('customer:create_job'))

        elif request.POST.get('step') == '2':
            step2_form = forms.JobCreateStep2Form(request.POST,
                                                  instance=creating_job)
            if step2_form.is_valid():
                creating_job = step2_form.save()

                return redirect(reverse('customer:create_job'))

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
                        f"&key={base.GOOGLE_MAP_API_KEY}")

                    # print(r.json()['rows'])
                    distance = r.json()['rows'][0]['elements'][0]['distance']['value']
                    duration = r.json()['rows'][0]['elements'][0]['duration']['value']
                    creating_job.distance = round(distance / 1000, 2)
                    creating_job.duration = int(duration / 60)
                    creating_job.price = round(creating_job.distance * 5, 2)
                    creating_job.save()
                except Exception as e:
                    print(e)
                    messages.error(request, "Error in google api")
                creating_job.status = Job.PROCESSING_STATUS
                creating_job.save()

                return redirect(reverse('customer:create_job'))

    if not creating_job:
        current_step = 1
    elif creating_job.pickup_name:
        current_step = 3
    else:
        current_step = 2

    return render(request, 'customer/create_job.html', {
        'google_map_api_key': base.GOOGLE_MAP_API_KEY,
        'job': creating_job,
        'step': current_step,
        'step1_form': step1_form,
        'step2_form': step2_form,
        'step3_form': step3_form,
    })


@login_required(login_url='/users/signin/?next=/customer/')
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


@login_required(login_url='/users/signin/?next=/customer/')
def job_page(request, job_id):
    job = Job.objects.get(id=job_id)

    if request.method == 'POST' and job.status == Job.PROCESSING_STATUS:
        job.status = Job.CANCELED_STATUS
        job.save()
        return redirect(reverse('customer:archived_jobs'))

    return render(request, 'customer/job.html', {
        'google_map_api_key': base.GOOGLE_MAP_API_KEY,
        'job': job
    })


@login_required(login_url='/users/signin/?next=/customer/')
def archived_jobs_page(request):
    jobs = Job.objects.filter(customer=request.user.customer,
                              status__in=[
                                  Job.COMPLETED_STATUS,
                                  Job.CANCELED_STATUS,
                              ])
    return render(request, 'customer/jobs.html', {
        'jobs': jobs
    })
