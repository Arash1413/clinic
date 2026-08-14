from django.shortcuts import render, redirect
from django.contrib import messages # برای نمایش پیام موفقیت
from .models import BlogCategory, GalleryCategory, GalleryItem, Service, Post, Appointment
from .forms import AppointmentForm
from django.shortcuts import get_object_or_404
import json
from django.http import JsonResponse
import jdatetime

def check_availability(request):
    date_str = request.GET.get('date')
    # پیدا کردن ساعت‌هایی که قبلاً برای این تاریخ رزرو شده‌اند
    booked_appointments = Appointment.objects.filter(date=date_str).values_list('time', flat=True)
    return JsonResponse({'booked_times': list(booked_appointments)})


def home(request):
    services = Service.objects.all()
    posts = Post.objects.all().order_by('-created_at')[:3]
    return render(request, 'index.html', {'services': services, 'posts': posts})

def service_detail(request, slug):
    service = Service.objects.get(slug=slug)
    return render(request, 'service_detail.html', {'service': service})


def book_appointment(request):
    services = Service.objects.all()
    
    # تولید لیست ۱۴ روز آینده
    today = jdatetime.date.today()
    days_list = []
    for i in range(14):
        date = today + jdatetime.timedelta(days=i)
        days_list.append({
            'j_date': date.strftime('%Y-%m-%d'), # برای ذخیره در دیتابیس
            'day_name': date.strftime('%A'),      # نام روز (مثلا شنبه)
            'day_num': date.day,                 # شماره روز (مثلا ۲۶)
            'month_name': date.strftime('%b'),   # نام ماه (مثلا مرداد)
        })

    return render(request, 'booking.html', {
        'services': services,
        'days_list': days_list
    })

def gallery_view(request, category_slug=None):
    categories = GalleryCategory.objects.all()
    selected_category = None
    items = GalleryItem.objects.all()

    if category_slug:
        selected_category = GalleryCategory.objects.get(slug=category_slug)
        items = items.filter(category=selected_category)

    return render(request, 'gallery.html', {
        'categories': categories,
        'items': items,
        'selected_category': selected_category
    })

def blog_list(request):
    posts = Post.objects.all().order_by('-created_at')
    categories = BlogCategory.objects.all()
    return render(request, 'blog_list.html', {'posts': posts, 'categories': categories})

def blog_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    post.view_count += 1 # افزایش تعداد بازدید با هر بار مشاهده
    post.save()
    recent_posts = Post.objects.exclude(id=post.id).order_by('-created_at')[:3]
    return render(request, 'blog_detail.html', {'post': post, 'recent_posts': recent_posts})


def service_detail(request, slug):
    # این خط سرویس را بر اساس اسلاگ پیدا می‌کند
    service = get_object_or_404(Service, slug=slug)
    return render(request, 'service_detail.html', {'service': service})


