""".env에서 SECRET 정보를 가져옴"""
from dotenv import load_dotenv
import os
load_dotenv()



""" import """
import requests
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .models import PofoloUser, User
from .serializers import UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny



############# function #############
"""JWT 발급 함수"""
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

"""로그인"""
@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    # 디버깅: 환경 변수 출력
    print("KAKAO_REST_API_KEY:", os.environ.get('KAKAO_REST_API_KEY'))  # REST API 키 출력
    print("KAKAO_REDIRECT_URI:", os.environ.get('KAKAO_REDIRECT_URI'))  # 리다이렉트 URI 출력
    # 프론트엔드에서 'code'를 받음
    code = request.data.get('code')

    if not code:
        return Response({"error": "Code not provided"}, status=status.HTTP_400_BAD_REQUEST)

    # 카카오 토큰 요청
    kakao_token_url = "https://kauth.kakao.com/oauth/token"
    data = {
        "grant_type": "authorization_code",
        "client_id": os.environ.get('KAKAO_REST_API_KEY'),
        "redirect_uri": os.environ.get('KAKAO_REDIRECT_URI'),
        "code": code
    }

    headers = {
    "Content-Type": "application/x-www-form-urlencoded;charset=utf-8"
    }

    token_response = requests.post(kakao_token_url, data=data)
    token_json = token_response.json()

    print(token_json)

    if "access_token" not in token_json:
        return Response({"error": "Failed to get access token"}, status=status.HTTP_400_BAD_REQUEST)

    access_token = token_json.get("access_token")   # 카카오 인증 서버로부터 받아온 액세스 토큰

    # 액세스 토큰으로 사용자 정보 가져오기
    user_info_url = "https://kapi.kakao.com/v2/user/me"
    headers = {"Authorization": f"Bearer {access_token}"}
    user_info_response = requests.get(user_info_url, headers=headers)
    user_info = user_info_response.json()

    kakao_id = user_info.get("id")

    # 사용자 생성 또는 로그인
    try:
        pofolo_user = PofoloUser.objects.get(kakao_id=kakao_id)
        # 기존 사용자, 로그인 처리 후 토큰 전달
        tokens = get_tokens_for_user(pofolo_user.user)
        return Response({
            "message": "로그인에 성공했습니다!",
            "user_id": pofolo_user.id,
            "access": tokens['access'],
            "refresh": tokens['refresh']
        }, status=status.HTTP_200_OK)
    except PofoloUser.DoesNotExist:
        # 신규 사용자, 회원가입 필요 안내와 함께 토큰 전달
        return Response({
            "message": "환영합니다! 회원가입을 완료해주세요!",
            "kakao_id": kakao_id
        }, status=status.HTTP_200_OK)


"""회원가입"""
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    # 프론트엔드로부터 회원가입 요청 데이터 받기
    kakao_id = request.data.get('kakao_id')
    nickname = request.data.get('nickname')
    education = request.data.get('education')
    main_field = request.data.get('main_field')

    # 필수 데이터가 모두 있는지 확인
    if not kakao_id or not nickname or not education or not main_field:
        return Response({"error": "All fields are required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # 이미 존재하는 사용자일 경우 오류 반환
        if PofoloUser.objects.filter(kakao_id=kakao_id).exists():
            return Response({"error": "User already registered"}, status=status.HTTP_400_BAD_REQUEST)

        # 새로운 사용자 생성
        # 기본 User 객체 생성
        user = User.objects.create(username=f"user_{kakao_id}")
      
        # PofoloUser 객체 생성 및 User와 연결
        pofolo_user = PofoloUser.objects.create(
            user=user,
            kakao_id=kakao_id,
            nickname=nickname,
            education=education,
            main_field=main_field
        )

        # JWT 발급
        tokens = get_tokens_for_user(user)
        return Response({
            "message": "회원가입 성공",
            "user_id": pofolo_user.id,
            "access": tokens['access'],
            "refresh": tokens['refresh']
        }, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


"""프로필 조회 및 수정"""
@api_view(['GET', 'PATCH'])
@permission_classes([IsAuthenticated])  # 인증된 사용자만 접근 가능
def manage_profile(request, user_id):
    user = get_object_or_404(PofoloUser, id=user_id)

    if request.user.id != user.id:
        return Response({"error": "권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)
    
    # 프로필 조회
    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response({
            "message": "프로필 조회 성공",
            "profile": serializer.data
        }, status=status.HTTP_200_OK)
    
    # 프로필 수정
    elif request.method == 'PATCH':
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "프로필이 성공적으로 수정되었습니다",
                "profile": serializer.data
            }, status=status.HTTP_200_OK)
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    

"""로그아웃"""
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    try:
        refresh = request.data.get("refresh")
        token = RefreshToken(refresh)
        token.blacklist()  # 토큰을 블랙리스트에 추가하여 무효화
        return Response({"message": "로그아웃 성공"}, status=status.HTTP_205_RESET_CONTENT)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)