from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .models import Post, Category
from .serializers import PostSerializer, CategorySerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


@api_view(['GET'])
def post_stats(request):
    total_posts = Post.objects.count()
    published_posts = Post.objects.filter(status='published').count()
    return Response({
        'total_posts': total_posts,
        'published_posts': published_posts
    })