from drf_spectacular.utils import OpenApiParameter, extend_schema
from drf_spectacular.types import OpenApiTypes

from rest_framework import status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.parsers import JSONParser

from recipes.models import Recipe
from recipes.serializers.recipe import RecipeSerializer

from .routes_permissions import IsOwnerOrReadOnly


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [IsOwnerOrReadOnly]

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="title",
                type=str,
                location=OpenApiParameter.QUERY,
                description="Filters recipes whose title contains this value (case-insensitive)",
            ),
            OpenApiParameter(
                name="username",
                type=str,
                location=OpenApiParameter.QUERY,
                description="Filters recipes by the author's username",
            ),
            OpenApiParameter(
                name="description",
                type=str,
                location=OpenApiParameter.QUERY,
                description="Filters recipes whose description contains this value (case-insensitive)",
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        queryset = Recipe.objects.all()

        fields = {
            "title": "title__icontains",
            "username": "user__username__icontains",
            "description": "description__icontains",
        }

        for key, value in fields.items():
            param = self.request.query_params.get(key, None)

            if param:
                queryset = queryset.filter(**{value: param})

        return queryset

    def perform_create(self, serializer) -> None:
        serializer.save(user=self.request.user)


@extend_schema(
    request=AuthTokenSerializer,
    responses={
        200: OpenApiTypes.OBJECT,
        400: OpenApiTypes.OBJECT,
    },
    description="Obtain an authentication token for a user.",
)
class CustomAuthToken(ObtainAuthToken):
    parser_classes = [JSONParser]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )

        if serializer.is_valid():
            user = serializer.validated_data["user"]
            token, _ = Token.objects.get_or_create(user=user)

            return Response(
                {"token": token.key, "user_id": user.id, "username": user.username}
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
