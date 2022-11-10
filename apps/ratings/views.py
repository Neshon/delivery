from django.contrib.contenttypes.models import ContentType
from django.shortcuts import HttpResponseRedirect

from .forms import RatingForm
from .models import Rating


def rate_object_view(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/')

    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            object_id_user = form.cleaned_data.get('object_id_user')
            object_id_job = form.cleaned_data.get('object_id_job')
            rating = form.cleaned_data.get('rating')
            content_type_user = form.cleaned_data.get('content_type_user')
            content_type_job = form.cleaned_data.get('content_type_job')
            c_type_user = ContentType.objects.get_for_id(content_type_user)
            c_type_job = ContentType.objects.get_for_id(content_type_job)
            obj = Rating.objects.create(
                content_type_user=c_type_user,
                object_id_user=object_id_user,
                content_type_job=c_type_job,
                object_id_job=object_id_job,
                value=rating,
                user=request.user
            )
            next_path = form.cleaned_data.get('next')

            return HttpResponseRedirect(next_path)

    return HttpResponseRedirect('/')
