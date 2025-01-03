from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import *

urlpatterns = [
    path('login/', login),
    path('nickname/', check_nickname),    # 닉네임 중복 확인
    path('register/', register),
    path('profile/<int:user_id>/', manage_profile, name='profile'),
    path('logout/', logout),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # 토큰 갱신 엔드포인트
    path('profile-img-upload/', UploadProfileImageView.as_view(), name='upload_profile_img'), #프로필 이미지 생성(업로드) 
    path('profile/image/<int:user_id>/', ManageProfileImageView.as_view(), name='manage_profile_img'), #프로필 수정/삭제 
]