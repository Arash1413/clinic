from django.urls import path
from . import views

urlpatterns = [
     path('', views.home, name='home'),
    path('book/', views.book_appointment, name='book_appointment'), # آدرس جدید
    path('gallery/', views.gallery_view, name='gallery'),
    path('blog/', views.blog_list, name='blog_list'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('gallery/<slug:category_slug>/', views.gallery_view, name='gallery_by_category'),
    path('service/<slug:slug>/', views.service_detail, name='service_detail'),
]