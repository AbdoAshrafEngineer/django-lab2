from django import forms
from .models import MyUser


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = MyUser
        fields = ["email", "username", "password"]

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")

        if password and password2 and password != password2:
            self.add_error("password2", "Passwords don't match")
        return cleaned_data

    def save(self, commit=True):
        # Override save to use the manager's create_user method
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.status = True
        if commit:
            user.save()
        return user
