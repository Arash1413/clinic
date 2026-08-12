from django.contrib import admin
from .models import Service, Post, Appointment, GalleryCategory, GalleryItem, BlogCategory

# ثبت مدل خدمات
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}

# ثبت مدل دسته‌بندی وبلاگ
@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}

# ثبت مدل مقالات وبلاگ
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'created_at')
    prepopulated_fields = {'slug': ('title',)}

# ثبت مدل نوبت‌دهی
@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone', 'service', 'date')
    list_filter = ('date', 'service')

# ثبت مدل دسته‌بندی گالری
@admin.register(GalleryCategory)
class GalleryCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}

# ثبت مدل آیتم‌های گالری
@admin.register(GalleryItem)
class GalleryItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'category')