from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from .models import ContactMessage, QuoteRequest, UserProfile


class ContactForm(forms.ModelForm):
    """فرم تماس"""
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Your name'),
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': _('Your email'),
                'required': True
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Phone (optional)')
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Subject'),
                'required': True
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': _('Your message'),
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
                'placeholder': _('Your name'),
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': _('Your email'),
                'required': True
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Phone number'),
                'required': True
            }),
            'company': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Company (optional)')
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': _('Project description'),
                'rows': 5,
                'required': True
            }),
            'budget': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Budget (optional)')
            }),
            'deadline': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Deadline (optional)')
            }),
        }


class UserRegistrationForm(UserCreationForm):
    """فرم ثبت‌نام کاربر"""
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': _('Email')
        })
    )
    first_name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('First name')
        })
    )
    last_name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Last name')
        })
    )
    phone = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Phone number')
        }),
        label=_('Phone number')
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Username')
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': _('Password')
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': _('Confirm password')
        })

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
            phone = self.cleaned_data.get('phone', '') or ''
            UserProfile.objects.update_or_create(user=user, defaults={'phone': phone})
        return user
