from django.shortcuts import render, redirect
from django.contrib import messages # برای نمایش پیام موفقیت
from .models import BlogCategory, GalleryCategory, GalleryItem, Service, Post
from .forms import AppointmentForm
from django.shortcuts import get_object_or_404

def home(request):
    services = Service.objects.all()
    posts = Post.objects.all().order_by('-created_at')[:3]
    return render(request, 'index.html', {'services': services, 'posts': posts})

def service_detail(request, slug):
    service = Service.objects.get(slug=slug)
    return render(request, 'service_detail.html', {'service': service})


def book_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'نوبت شما با موفقیت ثبت شد.')
            return redirect('home')
    else:
        form = AppointmentForm()
    return render(request, 'booking.html', {'form': form})


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


