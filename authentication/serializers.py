from rest_framework import serializers
from core.lib.serializers import make_serializer_class
from .models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.contrib import auth
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError, AuthenticationFailed


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    token = serializers.JSONField(read_only=True)
    email = serializers.EmailField(max_length=68, min_length=6, )

    class Meta:
        model = User
        fields = [
            "email",
            "password", "first_name",
            "token", "last_name",
        ]

    def validate(self, attrs):
        email = attrs.get('email', None)
        if User.objects.filter(email=email.lower()).exists():
            raise serializers.ValidationError({
                "email": _("this email is already exist")
            })

        return super().validate(attrs)

    def create(self, validated_data):
        user = User.objects.create_user(
            **validated_data
        )

        return user


class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    token = serializers.JSONField(read_only=True)
    email = serializers.EmailField(required=True, write_only=True)

    class Meta:
        model = User
        fields = [
            "password",
            'token', "email",
        ]

    def validate_email(self, attrs):
        email = attrs
        if not User.objects.filter(email=email).exists():
            raise ValidationError(_("User does not exist."))
        return attrs

    def validate(self, attrs):
        email = attrs.get("email", None)
        password = attrs.get("password", None)
        user = auth.authenticate(email=email, password=password)
        if not user:
            raise serializers.ValidationError({"password": "incorrect password"})
        tokens = user.get_tokens_for_user()

        return {
            "token": tokens,
        }


class ResetPasswordEmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)

    class Meta:
        fields = ["email"]


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=6, max_length=68, write_only=True)
    token = serializers.CharField(min_length=1, write_only=True)
    uidb64 = serializers.CharField(min_length=1, write_only=True)

    class Meta:
        fields = ["password", "token", "uidb64"]

    def validate(self, attrs):
        try:
            password = attrs.get("password")
            token = attrs.get("token")
            uidb64 = attrs.get("uidb64")
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed("The reset link is invalid", 401)

            user.set_password(password)
            user.save()

            return user
        except Exception as e:
            raise AuthenticationFailed("The reset link is invalid", 401)


UserInfoSer = make_serializer_class(User)
