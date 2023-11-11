from django.urls import path
from django.views.decorators.cache import cache_page

from blog.apps import BlogConfig
from blog.views import BlogPostListView, BlogPostDetailView, BlogPostCreateView, BlogPostUpdateView, BlogPostDeleteView

app_name = BlogConfig.name

urlpatterns = [
    path('', BlogPostListView.as_view(), name='blog_list'),
    path('detail/<slug>/', cache_page(60)(BlogPostDetailView.as_view()), name='blog_detail'),
    path('create/', BlogPostCreateView.as_view(), name='blog_create'),
    path('update/<slug>/', BlogPostUpdateView.as_view(), name='blog_update'),
    path('delete/<slug>/', BlogPostDeleteView.as_view(), name='blog_delete'),
]
