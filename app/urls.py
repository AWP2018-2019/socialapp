from django.conf.urls import url
from views import index, PostListView, post_detail

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^$', PostListView.as_view(), name='post_list'),
    url(r'^post/(?P<pk>[0-9]+)$', post_detail, name='post_detail'),
]