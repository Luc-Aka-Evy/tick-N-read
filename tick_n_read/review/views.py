from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from itertools import chain
from . import forms
from . import models
from authentication.models import User


@login_required
def home(request):

    users = []
    tickets = []
    reviews = []
    user_reviews = []

    user = models.UserFollows.objects.filter(user=request.user)
    answer = models.Review.objects.all()
    reviews_of_user = models.Review.objects.filter(user=request.user)


    for i in range(len(user)):
        users.append(user[i].followed_user)

    for i in range(len(users)):
        ticket = models.Ticket.objects.filter(user=users[i])
        review = models.Review.objects.filter(user=users[i])

        for i in range(len(ticket)):
            tickets.append(ticket[i])

        for i in range(len(review)):
            reviews.append(review[i])

    for answers in answer:
        if (
            answers.ticket.user == request.user
            and answers.user != request.user
            and answers.user not in users
        ):
            reviews.append(answers)

    
    for i in range(len(reviews_of_user)):
        user_reviews.append(reviews_of_user[i].ticket)

    tickets_and_reviews = sorted(
        chain(tickets, reviews),
        key=lambda instance: instance.time_created,
        reverse=True
    )
    
    
    paginator = Paginator(tickets_and_reviews, 6)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        "user_reviews": user_reviews,
        "page_obj": page_obj
    }
    return render(request, "review/home.html", context=context)


@login_required
def home_posts(request):
    tickets = models.Ticket.objects.filter(user=request.user).order_by("-time_created")

    reviews = models.Review.objects.filter(user=request.user).order_by("-time_created")

    tickets_and_reviews = sorted(
        chain(tickets, reviews),
        key=lambda instance: instance.time_created,
        reverse=True
    )

    paginator = Paginator(tickets_and_reviews, 6)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    

    context = {
        "page_obj": page_obj
    }
    return render(request, "review/my_posts.html", context=context)


@login_required
def view_ticket(request, ticket_id):
    comment_ticket = []
    user_reviews = models.Review.objects.filter(user=request.user)

    for i in range(len(user_reviews)):
        comment_ticket.append(user_reviews[i].ticket)

    ticket = get_object_or_404(models.Ticket, id=ticket_id)

    context = {
        "ticket": ticket,
        "commented": comment_ticket
    }
    return render(request, "review/view_ticket.html", context=context)


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
            edit_ticket = forms.TicketForm(request.POST, request.FILES, instance=ticket)
            if edit_ticket.is_valid():
                ticket_form = edit_ticket.save(commit=False)
                ticket_form.save()
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
            review.rating = review_form.cleaned_data["ratings"]
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
            review.rating = review_form.cleaned_data["ratings"]
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
                edit_review = edit_form.save(commit=False)
                edit_review.rating = edit_form.cleaned_data["ratings"]
                edit_review.save()
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
    following = []
    followers = []

    user = models.UserFollows.objects.filter(user=request.user)
    user_follower = models.UserFollows.objects.filter(followed_user=request.user)

    for i in range(len(user)):
        following.append(user[i].followed_user)

    for i in range(len(user_follower)):
        followers.append(user_follower[i].user)

    form = forms.FollowUsersForm()
    if request.method == "POST":
        form = forms.FollowUsersForm(request.POST)

        if form.is_valid():
            follow_user = models.UserFollows()
            follow_user.user = request.user
            follow_user.followed_user = User.objects.filter(
                username=form.cleaned_data["search"]
            ).get()
            follow_user.save()
        return redirect("home")

    context = {
        "following": following,
        "followers": followers,
        "form": form,
    }

    return render(request, "review/follow_users_form.html", context=context)


@login_required
def unfollow_users(request, user_id):
    user_follows = models.UserFollows.objects.filter(
        user=request.user, followed_user=user_id
    )
    follow = get_object_or_404(models.UserFollows, id=user_follows[0].id)
    unfollow = forms.DeleteFollowUsersForm()

    if request.method == "POST":
        unfollow = forms.DeleteFollowUsersForm(request.POST)
        if unfollow.is_valid():
            follow.delete()
        return redirect("home")

    context = {
        "user_follows": user_follows,
        "unfollow": unfollow,
    }

    return render(request, "review/unfollow_users_form.html", context=context)
