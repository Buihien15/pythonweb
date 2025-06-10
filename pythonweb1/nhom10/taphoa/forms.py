from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=30, required=True, label="Tên", widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=30, required=True, label="Họ", widget=forms.TextInput(attrs={'class': 'form-control'}))
    username = forms.CharField(label="Tên đăng nhập", widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label="Mật khẩu")
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label="Xác nhận mật khẩu")
    phone = forms.CharField(max_length=15, required=True, label="Số điện thoại", widget=forms.TextInput(attrs={'class': 'form-control'}))
    address = forms.CharField(max_length=100, required=True, label="Địa chỉ", widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'last_name', 'first_name', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            self.add_error('password2', "Mật khẩu xác nhận không khớp.")

class UserLoginForm(forms.Form):
    username = forms.CharField(label="Tên đăng nhập",widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label="Mật khẩu",) 