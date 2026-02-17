from django.urls import path
from django.views.generic.base import RedirectView
from . import views

# ─── 301 Redirects: آدرس‌های قدیمی سایت استاتیک (.html) → آدرس جدید (Django)
#     جلوگیری از از دست رفتن رتبه در گوگل وقتی URL عوض شده
urlpatterns = [
    path('index.html', RedirectView.as_view(url='/', permanent=True)),
    path('about.html', RedirectView.as_view(url='/about/', permanent=True)),
    path('contact.html', RedirectView.as_view(url='/contact/', permanent=True)),
    path('services.html', RedirectView.as_view(url='/services/', permanent=True)),
    path('packages.html', RedirectView.as_view(url='/packages/', permanent=True)),
    path('projects.html', RedirectView.as_view(url='/projects/', permanent=True)),
    path('resume.html', RedirectView.as_view(url='/resume/', permanent=True)),
    # ─── مسیرهای اصلی
    # Main pages
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('resume/', views.resume, name='resume'),
    
    # Services
    path('services/', views.services_list, name='services_list'),
    path('service/<slug:slug>/', views.service_detail, name='service_detail'),
    path('web-design/', views.web_design, name='web_design'),
    path('mobile-app/', views.mobile_app, name='mobile_app'),
    path('ecommerce/', views.ecommerce, name='ecommerce'),
    path('seo/', views.seo_services, name='seo_services'),
    path('hosting/', views.hosting_services, name='hosting_services'),
    path('ui-ux/', views.ui_ux_design, name='ui_ux_design'),
    
    # Packages
    path('packages/', views.packages_list, name='packages_list'),
    path('packages/compare/', views.packages_compare, name='packages_compare'),
    
    # Projects
    path('projects/', views.projects_list, name='projects_list'),
    path('project/<slug:slug>/', views.project_detail, name='project_detail'),
    
    # Blog
    path('blog/', views.blog_list, name='blog_list'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
    
    # Quote Request
    path('quote/', views.quote_request, name='quote_request'),
    
    # Authentication
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/edit/', views.edit_profile, name='edit_profile'),
    
    # Testimonials
    path('testimonials/', views.testimonials_list, name='testimonials_list'),
    
    # FAQ
    path('faq/', views.faq_list, name='faq_list'),
    
    # Newsletter
    path('newsletter/subscribe/', views.newsletter_subscribe, name='newsletter_subscribe'),
    
    # Process
    path('how-it-works/', views.how_it_works, name='how_it_works'),
    
    # Calculator
    path('calculator/', views.price_calculator, name='price_calculator'),
    
    # Technology Stack
    path('technology/', views.technology_stack, name='technology_stack'),
    
    # Legal Pages
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('terms-conditions/', views.terms_conditions, name='terms_conditions'),
    path('guarantee/', views.guarantee, name='guarantee'),
    
    # Sitemap
    path('sitemap/', views.sitemap, name='sitemap'),
    # Sitemap XML برای Google Search Console
    path('sitemap.xml', views.sitemap_xml, name='sitemap_xml'),
]
