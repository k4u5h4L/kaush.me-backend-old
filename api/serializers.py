from rest_framework import serializers
from datetime import datetime

from .models import Post, Comment, Contact
from users.models import CustomUser, Profile


class ProfileSerializer(serializers.ModelSerializer):
	class Meta:
		model = Profile
		fields = ['image']

class UserSerializer(serializers.ModelSerializer):
	profile = ProfileSerializer()
	class Meta:
		model = CustomUser

		# exclude = ('password',)
		fields = ['username', 'profile']
		depth = 1


class CommentSerializer(serializers.ModelSerializer):
	author = UserSerializer()
	class Meta:
		model = Comment
		fields = ['comment_text', 'comment_timestamp', 'author']
		depth = 1

	# def create(self, attrs):
    # instance = super(CommentSerializer, self).create(attrs)
    # instance.save()

class CommentCreateSerializer(serializers.ModelSerializer):
	class Meta:
		model = Comment
		fields = ['comment_text']
		# depth = 1

class ContactSerializer(serializers.ModelSerializer):
	class Meta:
		model = Contact
		fields = ['contact_name', 'contact_email', 'contact_message']
		# depth = 1


class PostSerializer(serializers.ModelSerializer):
	author = UserSerializer()
	# comments = serializers.PrimaryKeyRelatedField(many=True, queryset=Comment.objects.all(), write_only=True)
	comments = CommentSerializer(source='comment_set', many=True)

	post_timestamp = serializers.DateTimeField(format='%d %B %Y')

	class Meta:
		model = Post
		fields = ['id', 'author', 'image', 'post_title', 'post_text', 'post_timestamp', 'tags', 'comments']
		depth = 2