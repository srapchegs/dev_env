import re
from django import forms


class CreateReviewsForm(forms.Form):
    what_likes = forms.CharField()
    what_modern = forms.CharField()
    review = forms.CharField()

