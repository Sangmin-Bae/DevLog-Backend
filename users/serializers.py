from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from users.models import User
from users.validators.password import validate_password_policy


class SignUpSerializer(serializers.ModelSerializer):
    """
    Serializer for user signup.
    """

    email = serializers.EmailField(
        validators=[
            UniqueValidator(queryset=User.objects.all(), message="This email is already in use.")
        ]
    )
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["email", "nickname", "password1", "password2"]

    def validate_email(self, email):
        """
        이메일 중복 여부 검사
        """
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("This email is already in use.")
        return email

    def validate_nickname(self, nickname):
        """
        닉네임 중복 여부 검사
        """
        if User.objects.filter(nickname=nickname).exists():
            raise serializers.ValidationError("This nickname is already in use.")
        return nickname

    def validate_password1(self, password):
        """
        비밀번호 정책 검사
        """
        return validate_password_policy(password)

    def validate(self, data):
        """
        비밀번호 일치 여부 검사
        """
        password1 = data.get("password1")
        password2 = data.get("password2")

        if password1 != password2:
            raise serializers.ValidationError("Passwords do not match.")

        return data

    def create(self, validated_data):
        """
        유저 생성 및 비밀번호 해싱 후 사용자 객체 저장
        """
        password = validated_data.pop("password1")
        _ = validated_data.pop("password2", None)

        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

