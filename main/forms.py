from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import ContactMessage, QuoteRequest


class ContactForm(forms.ModelForm):
    """فرم تماس"""
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'نام شما',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'ایمیل شما',
                'required': True
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'شماره تماس (اختیاری)'
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'موضوع',
                'required': True
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'پیام شما',
                'rows': 5,
                'required': True
            }),
        }


class QuoteRequestForm(forms.ModelForm):
    """فرم درخواست قیمت"""
    SERVICE_CHOICES = [
        ('web_design', 'طراحی وبسایت'),
        ('mobile_app', 'طراحی اپلیکیشن موبایل'),
        ('ecommerce', 'فروشگاه اینترنتی'),
        ('seo', 'سئو و بهینه‌سازی'),
        ('hosting', 'هاستینگ و دامنه'),
        ('ui_ux', 'طراحی UI/UX'),
        ('custom', 'سفارشی'),
    ]
    
    PACKAGE_CHOICES = [
        ('basic', 'پکیج پایه'),
        ('commercial', 'پکیج تجاری'),
        ('professional', 'پکیج حرفه‌ای'),
        ('custom', 'پکیج کاستوم'),
    ]
    
    service_type = forms.ChoiceField(
        choices=SERVICE_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'required': True
        }),
        label='نوع خدمت'
    )
    
    package_type = forms.ChoiceField(
        choices=PACKAGE_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        label='نوع پکیج'
    )
    
    class Meta:
        model = QuoteRequest
        fields = ['name', 'email', 'phone', 'company', 'service_type', 'package_type', 
                  'description', 'budget', 'deadline']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'نام شما',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'ایمیل شما',
                'required': True
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'شماره تماس',
                'required': True
            }),
            'company': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'نام شرکت (اختیاری)'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'توضیحات پروژه',
                'rows': 5,
                'required': True
            }),
            'budget': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'بودجه تقریبی (اختیاری)'
            }),
            'deadline': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'مهلت پروژه (اختیاری)'
            }),
        }


class UserRegistrationForm(UserCreationForm):
    """فرم ثبت‌نام کاربر"""
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'ایمیل'
        })
    )
    first_name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'نام'
        })
    )
    last_name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'نام خانوادگی'
        })
    )
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'نام کاربری'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'رمز عبور'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'تکرار رمز عبور'
        })
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user
