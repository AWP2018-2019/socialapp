# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import render

from django.views import View
from django.views.generic import TemplateView, ListView, DetailView

from models import Post, UserProfile, User

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
    return render(request, "post_detail.html", {"post": post})

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
