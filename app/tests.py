# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase, Client
from django.urls import reverse

from app.models import Comment, Post, User, UserProfile

# Create your tests here.

class PostTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='user1', password='password'
        )
        self.post = Post.objects.create(
            text='Test post 1', 
            created_by=self.user
        )
        self.client = Client()
        self.client.force_login(user=self.user)
    
    def test_post_detail_returns_200(self):
        response = self.client.get(
            reverse('post_detail',
            kwargs={"pk": self.post.id})
        )
        self.assertEqual(response.status_code, 200)
        
    def test_post_detail_returns_correct_post(self):
        response = self.client.get(
            reverse('post_detail', 
            kwargs={"pk": self.post.id})
        )
        response_post = response.context['post']
        self.assertEqual(response_post, self.post)
    
    def test_post_delete_removes_object_from_database(self):
        response = self.client.post(
            reverse('post_delete', kwargs={"pk": self.post.id})
        )
        self.assertEqual(Post.objects.all().count(), 0)

class CommentTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='user1', password='password'
        )
        self.post = Post.objects.create(
            text='Test post 1', 
            created_by=self.user
        )
        self.client = Client()
        self.client.force_login(user=self.user)

    def test_comment_create(self):
        self.client.post(
            reverse('comment_create', kwargs={"pk": self.post.id}),
            data={"text": "Comment 1"}
        )
        comment =  Comment.objects.first()
        self.assertEqual(comment.text, "Comment 1")
        self.assertEqual(comment.created_by, self.user)
        self.assertEqual(comment.post, self.post)


class UserRelations(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='user1', password='pass1')
        UserProfile.objects.create(user=self.user)
        self.other_user = User.objects.create_user(
            username='user2', password='pass2')
        UserProfile.objects.create(user=self.other_user)
        self.client = Client()
        self.client.force_login(user=self.user)

    def test_send_friend_request(self):
        self.client.get(
            reverse("send_friend_request",
                    kwargs={"user_pk": self.other_user.id}
            )
        )
        self.assertIn(self.other_user, self.user.profile.friend_requests.all())