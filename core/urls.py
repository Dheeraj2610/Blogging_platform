from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView)
from .views import CreateblogView,RetriveblogView,UpdateblogView,DeleteblogView,ListblogView,userCreate,CommentDetail,CommentListForPost,CommentCreate,adminCreate,LogoutAPIView, DeleteCommentView

urlpatterns = [
   
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user-register/', userCreate.as_view(), name='user-register'),
    path('admin-users/create/', adminCreate.as_view(), name='admin-user-create'),
    path('create-blog/', CreateblogView.as_view(), name='create-blog'),
    path('retrive-blog/<int:pk>/', RetriveblogView.as_view(), name='Retrive-blog'),
    path('update-blog/<int:pk>/', UpdateblogView.as_view(), name='Update-blog'),
    path('delete-blog/<int:pk>/', DeleteblogView.as_view(), name='Delete-blog'),
    path('list-blog/',ListblogView.as_view(), name='List-blog'), 
    path('add-comment/<int:post_id>',CommentCreate.as_view(), name='comment'),
    path('posts/<int:post_id>/comments/', CommentListForPost.as_view(), name='comment-list-for-post'), 
    path('comment-delete/<int:post_id>/<int:comment_id>/', DeleteCommentView.as_view(), name='delete_comment'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    
    
  
]