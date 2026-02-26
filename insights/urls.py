from django.urls import path
from .views import CollectView
from .views_admin import admin_dashboard

app_name = 'insights'

urlpatterns = [
    path('collect/', CollectView.as_view(), name='collect'),
    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
]
