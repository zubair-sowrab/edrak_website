from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('services/', views.services_view, name='services'),
    path('projects/', views.projects_view, name='projects'),
    path('leases/', views.leases_view, name='leases'),
    path('about/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),

# Hidden Admin URLs
    path('admin-edrak/', views.custom_admin_dashboard, name='custom_admin'),
    path('admin-edrak/<str:item_type>/add/', views.item_form_view, name='item_add'),
    path('admin-edrak/<str:item_type>/edit/<int:pk>/', views.item_form_view, name='item_edit'),
    path('admin-edrak/<str:item_type>/delete/<int:pk>/', views.item_delete_view, name='item_delete'),
path('projects/<int:pk>/', views.project_detail_view, name='project_detail'),
    path('leases/<int:pk>/', views.lease_detail_view, name='lease_detail'),
path('admin-edrak/inquiry/action/', views.inquiry_action_view, name='inquiry_action'), # <-- Add this line
]

