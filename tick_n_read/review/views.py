from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from . import forms
from . import models


@login_required
def home(request):

    user = models.UserFollows.objects.get(user=request.user)

    ticket = models.Ticket.objects.filter(user=user.followed_user)

    review = models.Review.objects.filter(user=user.followed_user)

    context = {
        "ticket": ticket,
        "review": review,
    }
    return render(request, "review/home.html", context=context)


@login_required
def home_posts(request):
    ticket = models.Ticket.objects.filter(user=request.user)

    review = models.Review.objects.filter(user=request.user)

    context = {
        "ticket": ticket,
        "review": review,
    }
    return render(request, "review/my_posts.html", context=context)


@login_required
def view_ticket(request, ticket_id):
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    return render(request, "review/view_ticket.html", {"ticket": ticket})


@login_required
def post_ticket(request):
    ticket_form = forms.TicketForm()
    if request.method == "POST":
        ticket_form = forms.TicketForm(request.POST, request.FILES)
        if ticket_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()
        return redirect("home")

    context = {
        "ticket_form": ticket_form,
    }

    return render(request, "review/create_ticket.html", context=context)


@login_required
def edit_ticket(request, ticket_id):
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    edit_ticket = forms.TicketForm(instance=ticket)
    delete_ticket = forms.DeleteTicketForm()

    if request.method == "POST":
        if "edit_ticket" in request.POST:
            edit_form = forms.TicketForm(request.POST, instance=ticket)
            if edit_form.is_valid():
                edit_form.save()
                return redirect("home")
        elif "delete_ticket" in request.POST:
            delete_form = forms.DeleteTicketForm(request.POST)
            if delete_form.is_valid():
                ticket.delete()
                return redirect("home")

    context = {
        "edit_ticket": edit_ticket,
        "delete_ticket": delete_ticket,
    }

    return render(request, "review/edit_ticket.html", context=context)


@login_required
def post_review(request):
    review_form = forms.CreateReviewForm()
    ticket_form = forms.TicketForm()
    if request.method == "POST":
        review_form = forms.CreateReviewForm(request.POST)
        ticket_form = forms.TicketForm(request.POST, request.FILES)
        if all([review_form.is_valid(), ticket_form.is_valid()]):
            review = review_form.save(commit=False)
            review.ticket = ticket_form.save(commit=False)
            review.ticket.user = request.user
            review.user = request.user
            review.ticket.save()
            review.save()

        return redirect("home")

    context = {
        "ticket_form": ticket_form,
        "review_form": review_form,
    }

    return render(request, "review/create_review.html", context=context)


@login_required
def view_review(request, review_id):
    review = get_object_or_404(models.Review, id=review_id)
    return render(request, "review/view_review.html", {"review": review})


@login_required
def add_review_for_ticket(request, ticket_id):
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    review_form = forms.CreateReviewForm()
    if request.method == "POST":
        review_form = forms.CreateReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.ticket = ticket
            review.ticket.save()
            review.user = request.user
            review.save()

        return redirect("home")

    context = {
        "ticket": ticket,
        "review_form": review_form,
    }

    return render(request, "review/add_review.html", context=context)


@login_required
def edit_review(request, review_id):
    review = get_object_or_404(models.Review, id=review_id)
    edit_review = forms.CreateReviewForm(instance=review)
    delete_review = forms.DeleteReviewForm()

    if request.method == "POST":
        if "edit_review" in request.POST:
            edit_form = forms.CreateReviewForm(request.POST, instance=review)
            if edit_form.is_valid():
                edit_form.save()
                return redirect("home")
        elif "delete_review" in request.POST:
            delete_form = forms.DeleteReviewForm(request.POST)
            if delete_form.is_valid():
                review.delete()
                return redirect("home")

    context = {
        "edit_review": edit_review,
        "delete_review": delete_review,
    }
    return render(request, "review/edit_review.html", context=context)


@login_required
def follow_users(request):
    form = forms.FollowUsersForm()
    if request.method == "POST":
        form = forms.FollowUsersForm(request.POST)
        if form.is_valid():
            follow_form = form.save(commit=False)
            follow_form.user = request.user
            follow_form.save()

        return redirect("home")

    return render(request, "review/follow_users_form.html", context={"form": form})
