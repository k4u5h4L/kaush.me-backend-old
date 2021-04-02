from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from django.core.paginator import Paginator, EmptyPage

from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.response import Response
from ratelimit.decorators import ratelimit

from .serializers import PostSerializer, CommentSerializer, CommentCreateSerializer, ContactSerializer
from .models import Post
from .filters import PostFilter

# Create your views here.

cache_timeout = 60
paginate_number = 10

@api_view(['GET'])
@ratelimit(key='ip', rate='500/h')
def apiOverview(request):
	api_urls = {
		'Post detail':'/api/post/<int:postId>/',
		'List posts':'/api/posts/',
	}

	return Response(api_urls)

# @login_required(redirect_field_name='api-overview')
@api_view(['GET'])
@cache_page(cache_timeout)
@ratelimit(key='ip', rate='500/h')
def getPosts(request):
	posts = Post.objects.all().order_by('-id')

	paginate = Paginator(posts, paginate_number)
    # the paginator object takes in the full posts query, and the amount of posts per page

	page_num = request.GET.get('page', 1)
	try:
		page = paginate.page(page_num)
	except EmptyPage:
		# page = paginate.page(1)
		return Response([])

	posts = page

	serializer = PostSerializer(posts, many=True)
	# print(serializer.data)
	return Response(serializer.data)

@api_view(['GET'])
@cache_page(cache_timeout)
@ratelimit(key='ip', rate='500/h')
def getLatestPosts(request):
	posts = Post.objects.all().order_by('-post_timestamp')

	serializer = PostSerializer(posts[:4], many=True)
	# print(serializer.data)
	return Response(serializer.data)

@api_view(['GET'])
@cache_page(cache_timeout)
@ratelimit(key='ip', rate='500/h')
def getPostData(request, postId):
	try:
		post = Post.objects.get(id=postId)
	except Exception:
		return Response({"message": "Post not available"})
	post_serializer = PostSerializer(post)
	return Response(post_serializer.data)

@api_view(['POST'])
@cache_page(cache_timeout)
@login_required
@ratelimit(key='ip', rate='500/h')
def createComment(request, postId):
	try:
		post = Post.objects.get(id=postId)
	except Exception:
		return Response({"message": "Post not available"})
	
	comment_serializer = CommentCreateSerializer(data=request.data)
	if comment_serializer.is_valid():
		comment_serializer.save(author=request.user, parent_post=post)
		print('Comment has been saved')
	else:
		print(comment_serializer.errors)
	return Response(comment_serializer.data)

@api_view(['GET', 'POST'])
@renderer_classes([JSONRenderer])
def not_found_page(request, exception):
	return Response({"message": "Page not found"})

@api_view(['GET', 'POST'])
@renderer_classes([JSONRenderer])
def not_found_page_server(request):
	return Response({"message": "Page not found"})


@api_view(['POST'])
@cache_page(cache_timeout)
@ratelimit(key='ip', rate='500/h')
def receiveContact(request):
	print(request.data)
	contact_serializer = ContactSerializer(data=request.data)

	if contact_serializer.is_valid():
		contact_serializer.save()
		print('contact has been saved')
	else:
		print(contact_serializer.errors)
		return Response({'message': "Data which was sent was corrupted. Please don't send any funny stuff."})

	return Response({'message': "details have been saved in the DB"})

@api_view(['GET'])
@ratelimit(key='ip', rate='500/h')
def searchPosts(request):
	posts = Post.objects.all()

	postFilter = PostFilter(request.GET, queryset=posts)

	posts = postFilter.qs

	paginate = Paginator(posts, paginate_number)

	page_num = request.GET.get('page', 1)

	try:
		page = paginate.page(page_num)
	except EmptyPage:
		# page = paginate.page(1)
		return Response([])
      
	posts = page

	serializer = PostSerializer(posts, many=True)
	return Response(serializer.data)