from django.conf import settings
from django.contrib.auth import authenticate
from pathlib import Path

from django.apps import apps
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

MEDIA_ROOT = Path(settings.MEDIA_ROOT)


class TokenViewSet(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response({"error": "Username and password are required"}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, username=username, password=password)
        if user is not None:
            from rest_framework_simplejwt.tokens import RefreshToken

            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                }
            )

        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


class FileServeView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, app_label: str, model_name: str, pk: int, field_name: str):
        model = apps.all_models.get(app_label, {}).get(model_name)
        if model is None:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            instance = model.objects.get(pk=pk)
        except model.DoesNotExist:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)

        file_field = getattr(instance, field_name, None)
        if file_field is None or not file_field.name:
            return Response({"error": "No file"}, status=status.HTTP_404_NOT_FOUND)

        file_path = MEDIA_ROOT / file_field.name
        if not file_path.exists():
            return Response({"error": "File not found"}, status=status.HTTP_404_NOT_FOUND)

        from django.http import FileResponse

        return FileResponse(open(file_path, "rb"), as_attachment=True, filename=file_field.name)
