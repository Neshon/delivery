from django import forms

from .models import RatingChoices


class RatingForm(forms.Form):
    rating = forms.ChoiceField(widget=forms.RadioSelect(
        attrs={'class': 'rating__input'}),
        choices=RatingChoices.choices)
    object_id_user = forms.IntegerField(widget=forms.HiddenInput)
    content_type_user = forms.IntegerField(widget=forms.HiddenInput)
    object_id_job = forms.UUIDField(widget=forms.HiddenInput)
    content_type_job = forms.IntegerField(widget=forms.HiddenInput)
    next = forms.CharField(widget=forms.HiddenInput)
