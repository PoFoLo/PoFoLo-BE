from rest_framework import generics, permissions
from django.shortcuts import get_object_or_404
from .models import Portfolio, PofoloUser
from .serializers import PortfolioListSerializer, PortfolioDetailSerializer

# 포트폴리오 리스트 조회
class PortfolioListView(generics.ListAPIView):
    serializer_class = PortfolioListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Portfolio.objects.filter(is_public=True)
        user_id = self.kwargs.get('user_id')  # URL 경로에서 user_id를 가져옴

        if user_id:
            queryset = queryset.filter(writer__id=user_id)

        return queryset

# 포트폴리오 상세내용 조회/수정/삭제 
class PortfolioDetailView(generics.RetrieveAPIView):
    queryset = Portfolio.objects.all()
    serializer_class = PortfolioDetailSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'pk'

    def get_object(self):
        portfolio = super().get_object()
        portfolio.views += 1 #GET 요청시 조회수 증가 
        portfolio.save()
        return portfolio

    def perform_update(self, serializer):
        serializer.save()

# 포트폴리오 생성
class PortfolioCreateView(generics.CreateAPIView):
    serializer_class = PortfolioDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user = get_object_or_404(PofoloUser, user=self.request.user)
        serializer.save(writer=user)

# 포트폴리오 초대 URL 조회
class PortfolioInviteView(generics.RetrieveAPIView):
    queryset = Portfolio.objects.all()
    serializer_class = PortfolioDetailSerializer
    permission_classes = [permissions.AllowAny]  # 인증 없이 접근 가능

    def get_object(self):
        invite_url = self.kwargs['invite_url']
        portfolio = get_object_or_404(Portfolio, invite_url=invite_url)
        
        portfolio.views += 1 #인사팀 URL로 접근시 조회수 증가
        portfolio.save(update_fields=['views'])
        
        return portfolio