# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from django.views import View
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from forms import CommentForm, PostForm
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

class UserProfileView(DetailView):
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
        import pdb;pdb.set_trace();
        post = Post.objects.get(id=self.kwargs['pk'])
        Comment.objects.create(
            created_by=self.request.user, 
            post=post, 
            **form.cleaned_data
        )
        return redirect(reverse_lazy("post_detail", kwargs={"pk": self.kwargs['pk']}))

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
