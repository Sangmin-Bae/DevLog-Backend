from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from users.models import User


class UserCreationForm(forms.ModelForm):
    """신규 유저 생성 폼"""

    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password confirmation", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["email", "nickname"]

    def clean_password2(self):
        """password1과 password2가 일치하는지 검증하는 메서드"""
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise ValidationError("Password don't match")
        return password2

    def save(self, commit=True):
        """비밀번호 해싱 후 사용자 저장하는 save 오버라이드"""
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])

        if commit:
            user.save()

        return user


class UserChangeForm(forms.ModelForm):
    """유저 정보 수정 폼"""
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ["email", "nickname", "password", "is_active", "is_staff", "is_superuser", "groups", "user_permissions"]

    def clean_password(self):
        """비밀번호 필드의 초기값 반환"""
        return self.initial.get("password")

