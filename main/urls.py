from django.urls import path
from . import views

urlpatterns = [
    # Main pages
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('resume/', views.resume, name='resume'),
    path('team/', views.team, name='team'),
    
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
    
    # Language
    path('lang/<str:lang_code>/', views.set_language, name='set_language'),
]
