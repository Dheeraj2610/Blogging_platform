from email.mime.text import MIMEText
import smtplib
from django.shortcuts import render
from rest_framework import generics,status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from core.models import BlogPost,registration,User
from .serializers import blogCreateSerializer,blogSerializer,UserSerializer,CommentUpdateSerializer,userSerializer,ObtainTokenPairSerializer,CommentReadSerializer,CommentDeleteSerializer
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import Comment
from .serializers import CommentSerializer
from rest_framework.views import APIView
from django.http import JsonResponse    

class ObtainTokenPairView(TokenObtainPairView):
    serializer_class = ObtainTokenPairSerializer

# Create your views here.
class userCreate(generics.CreateAPIView):
    permission_classes = [IsAdminUser,IsAuthenticated]  # create user
    queryset = registration.objects.all()
    serializer_class = userSerializer

class adminCreate(generics.CreateAPIView):
    permission_classes = [IsAdminUser,IsAuthenticated]  # create admin
    queryset = registration.objects.all()
    serializer_class = UserSerializer

class CreateblogView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = BlogPost.objects.all()
    serializer_class = blogCreateSerializer

class RetriveblogView(generics.RetrieveAPIView):
    permission_classes = [IsAdminUser,IsAuthenticated]
    queryset = BlogPost.objects.all()
    serializer_class = blogSerializer

class UpdateblogView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = BlogPost.objects.all()
    serializer_class = blogSerializer

class DeleteblogView(generics.RetrieveDestroyAPIView):
    permission_classes = [IsAdminUser,IsAuthenticated]
    queryset = BlogPost.objects.all()
    serializer_class = blogSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "Blog deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

class ListblogView(generics.ListAPIView):
    permission_classes = [IsAdminUser,IsAuthenticated]
    queryset = BlogPost.objects.all()
    serializer_class =  blogSerializer




class CommentCreate(generics.CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    

    def post(self, request, post_id):
        try:
            post = BlogPost.objects.get(id=post_id)
        except BlogPost.DoesNotExist:
            return Response({'detail': 'Blog post does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=request.user, post=post)

        return Response(serializer.data, status=status.HTTP_201_CREATED)



class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAdminUser,IsAuthenticated]

    def get_queryset(self):
        author_id = self.kwargs['author']
        comment_id = self.kwargs['id']
        queryset = Comment.objects.filter(id=comment_id, author=author_id)
        return queryset




class CommentListForPost(generics.ListAPIView):
    serializer_class = CommentReadSerializer
    permission_classes = [IsAdminUser,IsAuthenticated]

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        return Comment.objects.filter(post_id=post_id)
    
    

class DeleteCommentView(generics.RetrieveDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    lookup_url_kwarg = 'comment_id'
    
    def get_object(self):
        post_id = self.kwargs['post_id']
        comment_id = self.kwargs['comment_id']
        return Comment.objects.get(id=comment_id, post_id=post_id)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "comment deleted successfully."}, status=status.HTTP_204_NO_CONTENT)



class LogoutAPIView(APIView):
    def post(self, request):
        response = JsonResponse({'message': 'Logout successful'})
        response.delete_cookie('jwt')
        return response