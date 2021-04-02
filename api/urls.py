from django.urls import path
from . import views

urlpatterns = [
	path('', views.apiOverview, name="api-overview"),
	path('contact/', views.receiveContact, name="contact-submit"),
	path('post/<int:postId>/', views.getPostData, name="get-post-data"),
	path('create/comment/<int:postId>/', views.createComment, name="create-reply"),
	path('posts/latest/', views.getLatestPosts, name="get-posts-latest"),
	path('posts/', views.getPosts, name="get-posts"),
	path('search/posts/', views.searchPosts, name="search-posts"),
]