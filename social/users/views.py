from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from .forms import UserRegistrationForm, UserUpdateForm, ProfileUpdateForm, SearchForm
from django.contrib.auth.models import User
from base.models import Post
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Contact
from notification.models import Notification
from django.contrib.postgres.search import (SearchVector,
                                            SearchQuery, SearchRank)


@login_required
@require_POST
def user_follow(request, username):

    user = get_object_or_404(User.objects.only('username'), username=username)

    if user:
        contact = Contact.objects.filter(user_from=request.user,
                                            user_to=user).first()

        if contact:
            Notification.objects.filter(notification_type=3, sender=contact.user_from, user=contact.user_to).delete()
            contact.delete()
            messages.success(request, f'You are no longer a subscriber to {user.username}')
        else:
            contact = Contact.objects.create(user_from=request.user,
                                    user_to=user)
            Notification.objects.create(notification_type=2, sender=contact.user_from, user=contact.user_to)
            messages.success(request, f'You have subscribed to {user.username}')

        return HttpResponseRedirect(reverse('users:user_detail', kwargs={'username': username}))


def user_detail(request, username):
    user = get_object_or_404(User.objects.select_related('profile').prefetch_related('followers')
                             .only('username', 'first_name', 'last_name', 'email',
                                                                         'profile__image', 'profile__bio'), username=username)
    posts = Post.objects.filter(author=user).only('title', 'date_posted', 'slug')

    context = {'user': user, 'posts': posts}
    return render(request, 'users/user_detail.html', context)


def user_search(request):
    # Получить все контакты, где текущий пользователь - user_from
    contacts_user_from = Contact.objects.filter(user_from=request.user)

    # Получить все контакты, где текущий пользователь - user_to
    contacts_user_to = Contact.objects.filter(user_to=request.user)

    followers = contacts_user_to.select_related('user_from__profile').only('user_from__profile__image',
                                                                           'user_from__profile__bio',
                                                                           'user_from__first_name',
                                                                           'user_from__last_name',
                                                                           'user_from__username',
                                                                           'user_from__profile__id')

    followers_users = [follower.user_from for follower in followers]

    friends = Contact.objects.filter(user_from=request.user, user_to__in=followers_users).select_related(
        'user_to__profile').only('user_to__profile__image',
                                 'user_to__profile__bio', 'user_to__first_name',
                                 'user_to__last_name', 'user_to__username', 'user_to__profile__id')

    friends_users = [friend.user_to for friend in friends]

    following_contacts = contacts_user_from.select_related('user_to__profile').only('user_to__profile__image',
                                                                         'user_to__profile__bio', 'user_to__first_name',
                                                                         'user_to__last_name', 'user_to__username', 'user_to__profile__id')
    
    following_users = [contact.user_to for contact in following_contacts]

    form = SearchForm()
    query = None
    results = []

    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = User.objects.filter(username__icontains=query).select_related('profile').only('profile__image', 'profile__bio',
                                                                                         'username', 'first_name', 'last_name')

    context = {'form': form, 'query': query,
               'results': results, 'following_users': following_users,
               'followers': followers_users, 'friends': friends_users}

    return render(request, 'users/users_list.html', context)


def register(request):
    context = {}
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account has been created! Welcome, {username}!')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    context['form'] = form
    return render(request, 'registration/register.html', context)

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                    request.FILES,
                                    instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Account has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {'u_form': u_form, 'p_form': p_form}
    return render(request, 'users/profile.html', context)
