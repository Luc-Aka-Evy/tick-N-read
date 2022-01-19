from django import forms
from django.db.models import fields

from . import models
from django.contrib.auth import get_user_model

User = get_user_model()


class TicketForm(forms.ModelForm):
    edit_ticket = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    class Meta:
        model = models.Ticket
        fields = ["title", "description", "image"]


class DeleteTicketForm(forms.Form):
    delete_ticket = forms.BooleanField(widget=forms.HiddenInput, initial=True)


class CreateReviewForm(forms.ModelForm):
    edit_review = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    class Meta:
        model = models.Review
        fields = ["rating", "headline", "body"]


class DeleteReviewForm(forms.Form):
    delete_review = forms.BooleanField(widget=forms.HiddenInput, initial=True)


class AddReviewForm(forms.ModelForm):
    class Meta:
        model = models.Review
        fields = ["ticket", "rating", "headline", "body"]


class FollowUsersForm(forms.ModelForm):
    class Meta:
        model = models.UserFollows
        fields = ["followed_user"]
