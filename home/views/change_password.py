from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        user = request.user
        old_password = request.data.get("old_password", "")
        new_password = request.data.get("new_password", "")
        confirm_password = request.data.get("confirm_password", "")

        errors = {}

        if not old_password:
            errors["old_password"] = "Current password is required."
        elif not user.check_password(old_password):
            errors["old_password"] = "Current password is incorrect."

        if not new_password:
            errors["new_password"] = "New password is required."
        elif new_password != confirm_password:
            errors["confirm_password"] = "New passwords do not match."
        else:
            try:
                validate_password(new_password, user=user)
            except ValidationError as e:
                errors["new_password"] = " ".join(e.messages)

        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save(update_fields=["password"])

        return Response({"success": True}, status=status.HTTP_200_OK)
