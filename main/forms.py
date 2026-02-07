from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from .models import ContactMessage, QuoteRequest, UserProfile, NewsletterSubscriber


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
    """Teklif formu — site sadece Türkçe"""
    SERVICE_CHOICES = [
        ('web_design', 'Web tasarımı'),
        ('mobile_app', 'Mobil uygulama tasarımı'),
        ('ecommerce', 'E-ticaret'),
        ('seo', 'SEO ve optimizasyon'),
        ('hosting', 'Hosting ve alan adı'),
        ('ui_ux', 'UI/UX tasarımı'),
        ('custom', 'Özel'),
    ]
    
    PACKAGE_CHOICES = [
        ('basic', 'Temel Paket'),
        ('commercial', 'Ticari Paket'),
        ('professional', 'Profesyonel Paket'),
        ('custom', 'Özel Paket'),
    ]
    
    service_type = forms.ChoiceField(
        choices=SERVICE_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'required': True
        }),
        label=_('Service type')
    )
    
    package_type = forms.ChoiceField(
        choices=PACKAGE_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        label=_('Package (optional)')
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
    """فرم ثبت‌نام کاربر — خطاها به انگلیسی برای الرت"""
    email = forms.EmailField(
        required=True,
        error_messages={'invalid': 'Enter a valid email address.', 'required': 'Email is required.'},
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': _('Email')})
    )
    first_name = forms.CharField(
        max_length=100, required=True,
        error_messages={'required': 'First name is required.'},
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('First name')})
    )
    last_name = forms.CharField(
        max_length=100, required=True,
        error_messages={'required': 'Last name is required.'},
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Last name')})
    )
    phone = forms.CharField(
        max_length=20, required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Phone number')}),
        label=_('Phone number')
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        widgets = {'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Username')})}
        error_messages = {
            'username': {'required': 'Username is required.'},
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].error_messages = {
            'required': 'Username is required.',
            'unique': 'A user with that username already exists.',
        }
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': _('Password')})
        self.fields['password1'].error_messages = {
            'required': 'Password is required.',
            'password_too_short': 'Password is too short.',
            'password_too_common': 'This password is too common.',
        }
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': _('Confirm password')})
        self.fields['password2'].error_messages = {
            'required': 'You must confirm your password.',
            'password_mismatch': 'The two password fields did not match.',
        }

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


class NewsletterForm(forms.ModelForm):
    """فرم ثبت‌نام در خبرنامه"""
    class Meta:
        model = NewsletterSubscriber
        fields = ['email', 'name']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': _('Your email address'),
                'required': True
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Your name (optional)')
            }),
        }
        labels = {
            'email': _('Email'),
            'name': _('Name'),
        }
