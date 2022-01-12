from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from . import forms


@login_required
def home(request):
    return render(request, "review/home.html")

@login_required
def post_ticket(request):
    ticket_form = forms.TicketForm()
    if request.method == 'POST':
        ticket_form = forms.TicketForm(request.POST, request.FILES)
        if ticket_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.save()
        return redirect('home')

    context = {
        'ticket_form': ticket_form,
    }

    return render(request, 'review/create_ticket.html', context=context)


@login_required
def post_review(request):
    review_form = forms.CreateReviewForm()
    ticket_form = forms.TicketForm()
    if request.method == 'POST':
        review_form = forms.CreateReviewForm(request.POST)
        ticket_form = forms.TicketForm(request.POST, request.FILES)
        if all([review_form.is_valid(), ticket_form.is_valid()]):
            review = review_form.save(commit=False)
            review.save()
            ticket = ticket_form.save(commit=False)
            ticket.save()
        return redirect('home')

    context = {
        'ticket_form': ticket_form,
        'review_form': review_form,
    }

    return render(request, 'review/create_review.html', context=context)
