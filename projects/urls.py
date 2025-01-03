from django.urls import path
from .views import (
   ProjectCreateAndImageUploadView, ProjectListView, ProjectDetailView,
   ProjectCreateAndImageUploadView, ProjectImageManageView,
   LinkTitleView, LikeProjectView, CommentListView, CommentDeleteView,
   MyProjectsView, LikedProjectView, CommentedProjectView
)

urlpatterns = [
    path('', ProjectListView.as_view(), name='project-list'),#프로젝트 리스트 조회
    path('<int:pk>/', ProjectDetailView.as_view(), name='project-detail'), # 프로젝트 세부사항 조회/수정/삭제
    path('create/', ProjectCreateAndImageUploadView.as_view(), name='project-create'),  # 프로젝트 생성
    path('<int:project_id>/images/', ProjectImageManageView.as_view()), # 이미지 수정   
    path('myproject/', MyProjectsView.as_view(), name='my-projects'), #내 프로젝트 조회
    path('liked/', LikedProjectView.as_view(), name='liked-projects'), #좋아요한 프로젝트 조회 
    path('commented/', CommentedProjectView.as_view(), name='commented-projects'), #댓글 단 프로젝트 조회
    path('<int:project_id>/like/', LikeProjectView.as_view(), name='like-projects'), #좋아요 누르기 
    path('<int:project_id>/comments/', CommentListView.as_view(), name='project-comment-create'), # 댓글(및 답글) 작성
    path('comments/<int:comment_id>/', CommentDeleteView.as_view(), name='project-comment-delete'), # 댓글 삭제
    path('links/', LinkTitleView.as_view(), name='link-title'),   # 링크를 받아 <title> 태그값을 반환
    path('watch/<int:writer>/', ProjectListView.as_view(), name='project-list') #다른사람 프로젝트 리스트 조회
]
