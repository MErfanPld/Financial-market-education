from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.hashers import make_password
from .models import User


class CustomUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="رمز عبور", widget=forms.PasswordInput)
    password2 = forms.CharField(label="تکرار رمز عبور", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("phone_number", "first_name", "last_name", "email")

    def clean_password2(self):
        p1 = self.cleaned_data.get("password1")
        p2 = self.cleaned_data.get("password2")
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("رمزها یکسان نیستند.")
        return p2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
    
    
    
    
class CustomUserChangeForm(forms.ModelForm):
    new_password = forms.CharField(
        label="رمز جدید",
        widget=forms.PasswordInput,
        required=False
    )

    class Meta:
        model = User
        fields = (
            "phone_number",
            "first_name",
            "last_name",
            "email",
            "image",
            "is_active",
            "is_staff",
            "is_superuser",
        )

    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data.get("new_password"):
            user.set_password(self.cleaned_data["new_password"])
        if commit:
            user.save()
        return user
