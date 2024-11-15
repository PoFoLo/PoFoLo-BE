from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .models import Project, TemporaryImage
from .serializers import ProjectListSerializer, ProjectDetailSerializer
from django.contrib.sessions.backends.db import SessionStore

# Main Page
# - 프로젝트 목록 조회
class ProjectListView(generics.ListAPIView):
    serializer_class = ProjectListSerializer

    def get_queryset(self):
        queryset = Project.objects.filter(is_public=True)
        field = self.request.query_params.get('field') #filtering with major_field 
        if field:
            queryset = queryset.filter(major_field=field)
        return queryset

# - 프로젝트 세부내용 조회
class ProjectDetailView(generics.RetrieveAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectDetailSerializer
    lookup_field = 'pk'

# - 프로젝트 생성
class ProjectCreateView(generics.CreateAPIView):
    serializer_class = ProjectDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(writer=self.request.user) #해당 사용자를 작성자(writer)로 지정


# - 프로젝트 이미지 추가
class ProjectImageUploadView(APIView):
    def post(self, request):
        session_key = request.session.session_key or request.session.create()  # 세션 키 생성
        image_urls = request.data.get('picture_urls', [])

        if len(image_urls) > 10:
            return Response({"error": "You can upload a maximum of 10 images."}, status=status.HTTP_400_BAD_REQUEST)

        for image_url in image_urls:
            TemporaryImage.objects.create(image_url=image_url, session_key=session_key)

        return Response({"message": "Images uploaded successfully.", "session_key": session_key}, status=status.HTTP_201_CREATED)

# - 프로젝트 수정/삭제
class ProjectUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectDetailSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'pk'

    def perform_update(self, serializer):
        serializer.save()

# MyPage
# - 내 프로젝트 조회
class MyProjectsView(generics.ListAPIView):
    serializer_class = ProjectListSerializer

    def get_queryset(self):
        queryset = Project.objects.filter(is_public=True)
        return queryset

# - 좋아요한 프로젝트 조회
class LikedProjectView(generics.ListAPIView):
    serializer_class = ProjectListSerializer

    def get_queryset(self):
        queryset = Project.objects.filter(is_public=True)
        return queryset

# - 코멘트한 프로젝트 조회
class CommentedProjectView(generics.ListAPIView):
    serializer_class = ProjectListSerializer

    def get_queryset(self):
        queryset = Project.objects.filter(is_public=True)
        return queryset