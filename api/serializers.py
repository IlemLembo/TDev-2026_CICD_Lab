from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User, Blog, Comment

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'is_verified', 'is_staff', 'is_active', 'password')
        read_only_fields = ('id', 'is_verified', 'is_staff', 'is_active')

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class LoginSerializer(TokenObtainPairSerializer):
    
    def validate(self, attrs):
        data = super().validate(attrs)

        user = self.user
        """
        if not user.is_verified:
            response = {
                "detail": "Votre compte n’a pas encore été vérifiée.",
            }
            return response
        """
        tokens = user.get_tokens()
        response = tokens
        return response

class BlogSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    class Meta:
        model = Blog
        fields = ('id', 'title', 'content', 'author', 'created_at', 'updated_at')
        read_only_fields = ('id', 'author', 'created_at', 'updated_at')

class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    blog = serializers.PrimaryKeyRelatedField(queryset=Blog.objects.all())
    class Meta:
        model = Comment
        fields = ('id', 'blog', 'author', 'content', 'created_at')
        read_only_fields = ('id', 'author', 'created_at')

