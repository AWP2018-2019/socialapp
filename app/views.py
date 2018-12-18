# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from django.views import View
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from forms import CommentForm, PostForm, UserProfileForm
from models import Post, UserProfile, User, Comment

# def index(request):
#     return HttpResponse("Welcome to the SocialApp!")


def index(request):
    post_list = Post.objects.all()
    return render(request, 'index.html', {'post_list': post_list})
    
# class PostListView(View):
    
#     def get(self, request, *args, **kwargs):
#         post_list = Post.objects.all()
#         return render(request, 'index.html', {'post_list': post_list})
        
# class PostListView(TemplateView):
#     template_name = 'index.html'
    
#     def get_context_data(self):
#         post_list = Post.objects.all()
#         context = {
#             'post_list': post_list
#         }
#         return context
        
class PostListView(ListView):
    template_name = 'index.html'
    model = Post
    context_object_name = 'post_list'
    
def post_detail(request, pk):
    post = Post.objects.get(id=pk)
    form = CommentForm()
    return render(request, "post_detail.html", 
    {"post": post, "form": form})

class UserProfileView(LoginRequiredMixin, DetailView):
    template_name = 'userprofile.html'
    model = UserProfile
    context_object_name = 'userprofile'

    def get_object(self):
        user = User.objects.get(id=self.kwargs['pk'])
        return user

class UserProfileRelationsView(DetailView):
    template_name = 'userprofilerelations.html'
    model = UserProfile
    context_object_name = 'userprofile'

    def get_object(self):
        user = User.objects.get(id=self.kwargs['pk'])
        return user

@login_required
def comment_create(request, pk):
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            post = Post.objects.get(id=pk)
            Comment.objects.create(
                created_by=request.user, 
                post=post, 
                **form.cleaned_data
            )
            return redirect(reverse_lazy("post_detail", kwargs={"pk": pk}))


class CommentCreateView(CreateView):
    model = Comment
    fields = ['text']
    
    def form_valid(self, form):
        post = Post.objects.get(id=self.kwargs['pk'])
        Comment.objects.create(
            created_by=self.request.user,
            post=post,
            **form.cleaned_data
        )
        return redirect(reverse_lazy("post_detail", kwargs={"pk": self.kwargs['pk']}))

class CommentEditView(UpdateView):
    model = Comment
    fields = ['text']
    pk_url_kwarg = 'pk_comment'
    template_name = 'comment_update.html'

    def form_valid(self, form):
        comment = Comment.objects.get(pk=self.kwargs['pk_comment'])
        comment.text = form.cleaned_data['text']
        comment.save()
        return redirect(reverse_lazy("post_detail", kwargs={"pk": self.kwargs['pk']}))

class CommentDeleteView(DeleteView):
    template_name = "comment_delete.html"
    model = Comment
    pk_url_kwarg = 'pk_comment'

    def get_success_url(self):
        return reverse_lazy("post_detail", kwargs={"pk": self.kwargs['pk']})


class PostCreateView(CreateView):
    model = Post
    fields = ['text']
    template_name = 'post_create.html'

    def form_valid(self, form):
        post = Post.objects.create(
            created_by=self.request.user,
            **form.cleaned_data
        )
        return redirect(reverse_lazy("post_detail", kwargs={"pk": post.id }))


def post_edit(request, pk):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = Post.objects.get(pk=pk)
            post.text = form.cleaned_data['text']
            post.save()
            return redirect(reverse_lazy("post_detail", kwargs={"pk": pk}))
    elif request.method == "GET":
        post = Post.objects.get(pk=pk)
        data= {"text": post.text}
        form = PostForm(initial=data)
        return render(request, "post_update.html",
                      {"post": post, "form":form})


class PostEditView(UpdateView):
    model = Post
    fields = ['text']
    template_name = 'post_update.html'

    def form_valid(self, form):
        post = Post.objects.get(pk=self.kwargs['pk'])
        post.text = form.cleaned_data['text']
        post.save()
        return redirect(reverse_lazy("post_detail", kwargs={"pk": self.kwargs['pk']}))


def post_delete(request, pk):
    if request.method == "POST":
        post = Post.objects.get(pk=pk)
        post.delete()
        return redirect(reverse_lazy("index"))
    elif request.method == "GET":
        post = Post.objects.get(pk=pk)
        return render(request, "post_delete.html",
                      {"post": post})


class PostDeleteView(DeleteView):
    template_name = "post_delete.html"
    model = Post

    def get_success_url(self):
        return reverse_lazy('index')


def accept_friend_request(request, user_pk):
    requesting_user = User.objects.get(pk=user_pk)
    request.user.profile.friends.add(requesting_user)
    requesting_user.profile.friends.add(request.user)
    requesting_user.profile.friend_requests.remove(request.user)
    request.user.profile.save()
    requesting_user.profile.save()
    return redirect(reverse_lazy("user_profile", kwargs={"pk": user_pk}))


class AcceptFriendRequestView(View):
    
    def get(self, request, *args, **kwargs):
        user_pk = self.kwargs['user_pk']
        requesting_user = User.objects.get(pk=user_pk)
        request.user.profile.friends.add(requesting_user)
        requesting_user.profile.friends.add(request.user)
        requesting_user.profile.friend_requests.remove(request.user)
        request.user.profile.save()
        requesting_user.profile.save()
        return redirect(reverse_lazy("user_profile", kwargs={"pk": user_pk}))


def reject_friend_request(request, user_pk):
    requesting_user = User.objects.get(pk=user_pk)
    requesting_user.profile.friend_requests.remove(request.user)
    requesting_user.profile.save()
    return redirect(reverse_lazy("user_profile", kwargs={"pk": user_pk}))

def cancel_friend_request(request, user_pk):
    requested_friend = User.objects.get(pk=user_pk)
    request.user.profile.friend_requests.remove(requested_friend)
    request.user.profile.save()
    return redirect(reverse_lazy("user_profile", kwargs={"pk": user_pk}))


class UnfriendView(View):

    def get(self, request, *args, **kwargs):
        friend_pk = self.kwargs['friend_pk']
        friend = User.objects.get(pk=friend_pk)
        request.user.profile.friends.remove(friend)
        friend.profile.friends.remove(request.user)
        request.user.profile.save()
        friend.profile.save()
        return redirect(reverse_lazy("user_profile", kwargs={"pk": friend_pk}))

class SendFriendRequestView(View):

    def get(self, request, *args, **kwargs):
        requested_user_pk = self.kwargs['user_pk']
        requested_user = User.objects.get(pk=requested_user_pk)
        request.user.profile.friend_requests.add(requested_user)
        request.user.profile.save()
        return redirect(reverse_lazy("user_profile",
                                    kwargs={"pk": requested_user_pk}))

class UserProfileUpdateView(UpdateView):
    model = UserProfile
    form_class = UserProfileForm
    template_name = 'profile_update.html'

    def get_context_data(self, **kwargs):
        context = super(UserProfileUpdateView, self).get_context_data(**kwargs)
        user =  self.object.user
        context['form'].fields['first_name'].initial = user.first_name
        context['form'].fields['last_name'].initial = user.last_name
        context['form'].fields['e_mail'].initial = user.email
        return context

    def form_valid(self, form):
        data = form.cleaned_data
        self.object.birthday = data['birthday']
        self.object.country_id = data['country']
        self.request.user.first_name = data['first_name']
        self.request.user.last_name = data['last_name']
        self.request.user.email = data['e_mail']
        self.object.save()
        self.request.user.save()
        return redirect(reverse_lazy("user_profile",
                                     kwargs={"pk": self.request.user.id}))


class RegisterView(CreateView):
    template_name= 'register.html'
    form_class = UserCreationForm
    model = User

    def form_valid(self, form):
        data = form.cleaned_data
        user = User.objects.create_user(username=data['username'],
                                        password=data['password1'])
        UserProfile.objects.create(user=user)
        return redirect('index')

class LoginView(TemplateView):
    template_name = 'login.html'

    def get_context_data(self):
        form = AuthenticationForm()
        return {'form': form}

    def post(self, request, *args, **kwargs):
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(username=data['username'],
                                password=data['password'])
            login(request, user)
            return redirect(reverse_lazy('index'))
        else:
            return render(request, "login.html", {"form": form})
