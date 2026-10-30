from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.response import Response

from .models import Blog, Comment, User
from .serializers import (
    BlogSerializer,
    CommentSerializer,
    LoginSerializer,
)


# Create your views here.
class LoginViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = LoginSerializer
    http_method_names = ["post"]

    @swagger_auto_schema(
        operation_description="Obtain a new access and refresh token pair using user credentials.",
        name="login",
        request_body=LoginSerializer,
        tags=["Authentification"],
        responses={
            200: "Access and refresh tokens successfully obtained.",
            400: "Invalid credentials or request data.",
        },
    )
    def create(self, request, *args, **kwargs):
        """
        Handle POST request to obtain a new access and refresh token pair.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    http_method_names = ["get", "post", "put", "delete"]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)

    def perform_destroy(self, instance):
        instance.delete()

    def get_queryset(self):
        queryset = super().get_queryset()
        author_id = self.request.query_params.get("author_id")
        if author_id:
            queryset = queryset.filter(author__id=author_id)
        return queryset

    @swagger_auto_schema(
        operation_summary="Récupère la liste des blogs",
        operation_description="Récupère la liste des blogs",
        responses={200: BlogSerializer(many=True)},
    )
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Récupère un blog",
        operation_description="Récupère un blog",
        responses={200: BlogSerializer()},
    )
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Crée un blog",
        operation_description="Crée un blog",
        request_body=BlogSerializer,
        responses={201: BlogSerializer()},
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)

    @swagger_auto_schema(
        operation_summary="Met à jour un blog",
        manual_parameters=[
            openapi.Parameter(
                "id",
                openapi.IN_PATH,
                description="ID du blog à mettre à jour",
                required=True,
                type=openapi.TYPE_INTEGER,
            )
        ],
        operation_description="Met à jour un blog",
        request_body=BlogSerializer,
        responses={200: BlogSerializer()},
    )
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Supprime un blog",
        operation_description="Supprime un blog",
        responses={204: "Supprimé"},
    )
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=204)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    http_method_names = ["get", "post", "put", "delete"]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
