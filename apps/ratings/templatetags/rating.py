from django import template
from django.contrib.contenttypes.models import ContentType

from apps.ratings.forms import RatingForm
from apps.ratings.models import Rating

register = template.Library()


@register.inclusion_tag('ratings/rating.html', takes_context=True)
def rating(context, *args, **kwargs):
    obj = kwargs.get('object')
    role = kwargs.get('role')
    app_label_courier = obj.courier._meta.app_label
    model_name_courier = obj.courier._meta.model_name

    if role == 'customer':
        request = context['request']
        customer = request.user
        app_label_job = obj._meta.app_label
        model_name_job = obj._meta.model_name
        c_type_courier = ContentType.objects.get(app_label=app_label_courier,
                                                 model=model_name_courier)
        c_type_job = ContentType.objects.get(app_label=app_label_job,
                                             model=model_name_job)
        try:
            rating_courier = Rating.objects.get(
                user=customer,
                content_type_job=c_type_job,
                object_id_job=obj.id,
            )
        except:
            context['form'] = RatingForm(initial={
                'object_id_user': obj.courier.id,
                'content_type_user': c_type_courier.id,
                'object_id_job': obj.id,
                'content_type_job': c_type_job.id,
                'next': request.path,
            })
        else:
            rated = rating_courier.value
            context = {
                'rated': f'You rated {rated} stars'
            }
    elif role == 'courier':
        c_type_courier = ContentType.objects.get(app_label=app_label_courier,
                                                 model=model_name_courier)
        avg_rating = Rating.objects.filter(content_type_user=c_type_courier,
                                           object_id_user=obj.courier.id,
                                           ).rating()
        if avg_rating:
            context = {
                'avg_rating': f'{avg_rating} / 5',
            }
        else:
            context = {
                'avg_rating': 'No rating',
            }
    return context
