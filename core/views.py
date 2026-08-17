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
    service_id = request.GET.get('service_id')
    
    # پیدا کردن پزشکِ مربوط به این خدمت
    service = get_object_or_404(Service, id=service_id)
    doctor = service.doctor
    
    # فیلتر کردن نوبت‌ها: فقط نوبت‌های همین "پزشک" در این "تاریخ"
    # با این کار نوبت‌های پزشکان دیگر در خدمات دیگر تاثیری روی این پزشک ندارد
    booked_appointments = Appointment.objects.filter(
        date=date_str, 
        doctor=doctor
    ).values_list('time', flat=True)
    
    return JsonResponse({'booked_times': list(booked_appointments)})

def home(request):
    services = Service.objects.all()
    posts = Post.objects.all().order_by('-created_at')[:3]
    return render(request, 'index.html', {'services': services, 'posts': posts})

def service_detail(request, slug):
    # لود کردن خدمت به همراه اطلاعات پزشک برای کاهش تعداد کوئری‌ها
    service = get_object_or_404(Service.objects.select_related('doctor'), slug=slug)
    return render(request, 'service_detail.html', {'service': service})


def book_appointment(request):
    # دریافت آیدی خدمتی که کاربر در صفحه اصلی انتخاب کرده است
    service_id = request.GET.get('service_id')
    # اگر آیدی نبود، اولین خدمت را به عنوان پیش‌فرض بگیر (یا می‌توانید خطا بدهید)
    selected_service = get_object_or_404(Service, id=service_id) if service_id else Service.objects.first()

    if request.method == 'POST':
        date = request.POST.get('date')
        time = request.POST.get('time')
        # گرفتن آیدی خدمت از فرم پنهان
        s_id = request.POST.get('service_id')
        
        if date and time and s_id:
            request.session['booking_date'] = date
            request.session['booking_time'] = time
            request.session['booking_service_id'] = s_id
            return redirect('booking_info') # رفتن به مرحله وارد کردن نام و تلفن
        
    # تولید لیست ۱۴ روز آینده
    today = jdatetime.date.today()
    days_list = []
    for i in range(14):
        date = today + jdatetime.timedelta(days=i)
        days_list.append({
            'j_date': date.strftime('%Y-%m-%d'),
            'day_name': date.strftime('%A'),
            'day_num': date.day,
        })

    return render(request, 'booking.html', {
        'days_list': days_list,
        'pre_selected_service': selected_service
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

def booking_info(request):
    # چک کردن اینکه آیا کاربر مرحله قبل را انجام داده یا خیر
    booking_date = request.session.get('booking_date')
    booking_time = request.session.get('booking_time')
    
    if not booking_date or not booking_time:
        return redirect('book_appointment')

    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            # اضافه کردن تاریخ و ساعت از سشن به مدل قبل از ذخیره نهایی
            appointment.date = booking_date
            appointment.time = booking_time
            appointment.save()
            
            # پاک کردن سشن بعد از ثبت موفق
            del request.session['booking_date']
            del request.session['booking_time']
            
            messages.success(request, f"نوبت شما برای تاریخ {booking_date} ساعت {booking_time} ثبت شد.")
            return redirect('home')
    else:
        form = AppointmentForm()

    return render(request, 'booking_info.html', {
        'form': form,
        'date': booking_date,
        'time': booking_time
    })


