from django import forms
from django.core import validators
from django.forms import widgets
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from .models import Ticket, Review


class TicketForm(forms.ModelForm):
    edit_ticket = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    class Meta:
        model = Ticket
        fields = ["title", "description", "image"]
        labels = {"title": "Titre"}


class DeleteTicketForm(forms.Form):
    delete_ticket = forms.BooleanField(widget=forms.HiddenInput, initial=True)


class CreateReviewForm(forms.ModelForm):
    edit_review = forms.BooleanField(widget=forms.HiddenInput, initial=True)
    rating_choices = [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5)]
    ratings = forms.ChoiceField(
        label="Notes", choices=rating_choices, widget=forms.RadioSelect
    )

    class Meta:
        model = Review
        fields = ["headline", "body"]
        labels = {"rating": "Notes", "headline": "Titre", "body": "Commentaires"}
        widgets = {"body": forms.Textarea}


class DeleteReviewForm(forms.Form):
    delete_review = forms.BooleanField(widget=forms.HiddenInput, initial=True)


class AddReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["ticket", "rating", "headline", "body"]


class FollowUsersForm(forms.Form):
    search = forms.CharField(label="Nom d'utilisateur:")


class DeleteFollowUsersForm(forms.Form):
    unfollow = forms.BooleanField(widget=forms.HiddenInput, initial=True)
