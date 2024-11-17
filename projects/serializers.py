from rest_framework import serializers
from .models import Project, TemporaryImage, Like, Comment, PofoloUser
from django.shortcuts import get_object_or_404


class ProjectListSerializer(serializers.ModelSerializer):
    thumbnail = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ['id', 'writer', 'title', 'major_field', 'sub_field',
        'liked_count', 'comment_count', 'thumbnail', 'created_at']

    def get_thumbnail(self, obj):
        #FIX - None 대신 디폴트 이미지 url 첨부해야됨. 
        return obj.picture_urls[0] if obj.picture_urls else None 

class ProjectDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'writer', 'title', 'description', 'major_field', 'sub_field','tags', 'skills', 'links', 
                'picture_urls', 'created_at', 'is_public', 'liked_count', 'comment_count', 'views']
        read_only_fields = ['id', 'writer', 'created_at', 'liked_count', 'comment_count', 'views']
        # - 변경 불가 항목들

    def get_object(self):
        project = super().get_object()
        project.views += 1 #GET 요청시 조회수 증가 
        project.save()
        return project
    
    def validate_title(self, value):
        if not value:
            raise serializers.ValidationError("Title is required.")
        return value

    def validate_description(self, value):
        if not value:
            raise serializers.ValidationError("Description is required.")
        return value

    def validate_field(self, value):
        if not value:
            raise serializers.ValidationError("Field is required.")
        return value
    
    def create(self, validated_data):
        session_key = self.context['request'].data.get('session_key') # 세션 키로 TemporaryImage 가져오기

        if session_key:
            temporary_images = TemporaryImage.objects.filter(session_key=session_key)
            picture_urls = [img.image_url for img in temporary_images]
            validated_data['picture_urls'] = picture_urls[:10]  # 최대 10개
            temporary_images.delete() # default 이미지 삭제

        return super().create(validated_data)


"""댓글"""
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'writer', 'project', 'commented_at', 'text', 'parent_comment']
        read_only_fields = ['writer', 'commented_at', 'project'] # 작성자, 작성시간 수정 불가
    
    def create(self, validated_data):
        request = self.context.get('request')
        user = get_object_or_404(PofoloUser, user=request.user)
        validated_data['writer'] = user
        return super().create(validated_data)
