from django import forms
from django.forms import widgets
from . import models


class TicketForm(forms.ModelForm):
    edit_ticket = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    class Meta:
        model = models.Ticket
        fields = ["title", "description", "image"]
        labels = {'title': 'Titre'}


class DeleteTicketForm(forms.Form):
    delete_ticket = forms.BooleanField(widget=forms.HiddenInput, initial=True)


class CreateReviewForm(forms.ModelForm):
    edit_review = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    class Meta:
        model = models.Review
        fields = ["rating", "headline", "body"]
        labels = {'rating': 'Notes', 'headline': 'Titre', 'body': 'Commentaires'}
        widgets = {'body': forms.Textarea}


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
        labels = {'followed_user': 'nom d''utilisateur'}
        widgets = {'followed_user': forms.TextInput}
               

class DeleteFollowUsersForm(forms.Form):
    unfollow = forms.BooleanField(widget=forms.HiddenInput, initial=True)