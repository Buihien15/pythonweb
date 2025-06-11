from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import StoreReview

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label="Email",
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'autocomplete': 'off',
            'name': 'new_email',
            'id': 'new_email'
        })
    )
    first_name = forms.CharField(
        max_length=30,
        required=True,
        label="Tên",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'autocomplete': 'off'
        })
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        label="Họ",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'autocomplete': 'off'
        })
    )
    username = forms.CharField(
        label="Tên đăng nhập",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'autocomplete': 'off',
            'name': 'new_username',   # tên giả
            'id': 'new_username'      # id giả
        })
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'autocomplete': 'new-password',
            'name': 'new_password1',
            'id': 'new_password1'
        }),
        label="Mật khẩu"
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'autocomplete': 'new-password',
            'name': 'new_password2',
            'id': 'new_password2'
        }),
        label="Xác nhận mật khẩu"
    )
    phone = forms.CharField(
        max_length=15,
        required=True,
        label="Số điện thoại",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'autocomplete': 'off'
        })
    )
    address = forms.CharField(
        max_length=100,
        required=True,
        label="Địa chỉ",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'autocomplete': 'off'
        })
    )

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

# Các form còn lại cũng nên thêm autocomplete nếu cần
class UserLoginForm(forms.Form):
    username = forms.CharField(
        label="Tên đăng nhập",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'autocomplete': 'off',
            'name': 'new_username',
            'id': 'new_username'
        })
    )
    password = forms.CharField(
        label="Mật khẩu",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'autocomplete': 'new-password',
            'name': 'new_password',
            'id': 'new_password'
        })
    )

class NewsSearchForm(forms.Form):
    query = forms.CharField(
        label='Tìm tiêu đề',
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'autocomplete': 'off'})
    )

class StoreReviewForm(forms.ModelForm):
    class Meta:
        model = StoreReview
        fields = ['name', 'email', 'rating', 'comment']
        labels = {
            'name': 'Họ và Tên',
            'email': 'Email',
            'rating': 'Số sao đánh giá',
            'comment': 'Nội dung đánh giá',
        }
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 4, 'autocomplete': 'off'}),
            'name': forms.TextInput(attrs={'autocomplete': 'off'}),
            'email': forms.EmailInput(attrs={'autocomplete': 'off'}),
            'rating': forms.NumberInput(attrs={'autocomplete': 'off'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.initial.get('name'):
            self.fields['name'].widget.attrs['readonly'] = True
        if self.initial.get('email'):
            self.fields['email'].widget.attrs['readonly'] = True
