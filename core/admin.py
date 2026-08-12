from django.contrib import admin
from .models import Service, Post, Appointment, GalleryCategory, GalleryItem

# شخصی‌سازی نحوه نمایش خدمات در پنل مدیریت
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug') # ستون‌هایی که در لیست نمایش داده می‌شود
    prepopulated_fields = {'slug': ('title',)} # ساخت خودکار اسلاگ از روی عنوان

# نمایش مقالات وبلاگ
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title', 'summary') # قابلیت جستجو در مقالات

# نمایش نوبت‌های رزرو شده
@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone', 'service', 'date')
    list_filter = ('date', 'service') # فیلتر کردن نوبت‌ها بر اساس تاریخ و نوع خدمت




@admin.register(GalleryCategory)
class GalleryCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}

@admin.register(GalleryItem)
class GalleryItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'category')
    list_filter = ('category',)