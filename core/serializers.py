from rest_framework import serializers
from core.models import BlogPost,Comment,registration
from django.contrib.auth.models import User
from django.core.mail import send_mail
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class ObtainTokenPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['email'] = user.email

        return token
    
class userSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )

        # Send confirmation email to user
        subject = 'Welcome to My Blog!'
        message = f'Hi {user.username}, thanks for registering on My Blog.'
        from_email = 'blogger@example.com'
        recipient_list = [user.email]
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)

        return user
    
class UserSerializer(serializers.ModelSerializer):
    is_staff = serializers.BooleanField(default=False)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'is_staff')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            is_staff=validated_data.get('is_staff', False),
            is_superuser=False
        )

        subject = 'Welcome to My Blog!'
        message = f'Hi {user.username}, thanks for registering on My Blog.'
        from_email = 'blogger@example.com'
        recipient_list = [user.email]
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)

        return user



class blogCreateSerializer(serializers.ModelSerializer):
    lookup_field = 'pk'
    class Meta:
        model = BlogPost
        fields = '__all__'

class blogSerializer(serializers.ModelSerializer):
    lookup_field = 'pk'
    class Meta:
        model = BlogPost
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = Comment
        fields = ('id', 'content', )

class CommentReadSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = Comment
        fields = '__all__'



class CommentUpdateSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = Comment
        fields = ('content',)

class CommentDeleteSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = Comment
        fields = ('content',)



    
