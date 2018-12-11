from django.conf.urls import url
from views import (
    index,
    PostListView,
    post_detail,
    UserProfileView,
    UserProfileRelationsView
)

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^$', PostListView.as_view(), name='post_list'),
    url(r'^post/(?P<pk>[0-9]+)$', post_detail, name='post_detail'),
    url(r'^userprofile/(?P<pk>[0-9]+)$', UserProfileView.as_view(),
        name='user_profile'),
    url(r'^userprofile/(?P<pk>[0-9]+)/relations$', UserProfileRelationsView.as_view(),
        name='user_profile_relations'),
]
