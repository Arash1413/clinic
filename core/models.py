from django.db import models
from django.utils.text import slugify
from django.urls import reverse

# ۱. مدل پزشک (پایه اصلی پروژه)
class Doctor(models.Model):
    name = models.CharField(max_length=100, verbose_name="نام پزشک")
    specialty = models.CharField(max_length=100, verbose_name="تخصص")
    image = models.ImageField(upload_to='doctors/', verbose_name="تصویر پزشک")

    class Meta:
        verbose_name = "پزشک"
        verbose_name_plural = "پزشکان"

    def __str__(self):
        return self.name

# ۲. مدل خدمات (متصل به پزشک)
class Service(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='services', verbose_name="پزشک مربوطه")
    title = models.CharField(max_length=200, verbose_name="نام خدمت (مثلاً کراتین مو)")
    image = models.ImageField(upload_to='services/', verbose_name="تصویر خدمت")
    slug = models.SlugField(unique=True, verbose_name="شناسه در آدرس (انگلیسی)")
    description = models.TextField(verbose_name="توضیحات کامل خدمت")

    class Meta:
        verbose_name = "خدمت"
        verbose_name_plural = "خدمات"

    def __str__(self):
        return f"{self.title} ({self.doctor.name})"

    def get_absolute_url(self):
        return reverse('service_detail', kwargs={'slug': self.slug})

# ۳. مدل نوبت‌دهی (مدیریت تداخل نوبت هر پزشک)
class Appointment(models.Model):
    TIME_CHOICES = [
        ('10:00', '10:00'), ('10:30', '10:30'),
        ('11:00', '11:00'), ('11:30', '11:30'),
        ('16:00', '16:00'), ('16:30', '16:30'),
        ('17:00', '17:00'), ('17:30', '17:30'),
        ('18:00', '18:00'), ('18:30', '18:30'),
    ]

    full_name = models.CharField(max_length=100, verbose_name="نام بیمار")
    phone = models.CharField(max_length=15, verbose_name="شماره تماس")
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, verbose_name="پزشک")
    service = models.ForeignKey(Service, on_delete=models.CASCADE, verbose_name="خدمت")
    date = models.DateField(verbose_name="تاریخ نوبت")
    time = models.CharField(max_length=5, choices=TIME_CHOICES, verbose_name="ساعت نوبت")
    message = models.TextField(blank=True, null=True, verbose_name="توضیحات")

    class Meta:
        # جلوگیری از تداخل: هر دکتر در یک تاریخ و ساعت فقط یک نوبت می‌تواند داشته باشد
        unique_together = ('doctor', 'date', 'time')
        verbose_name = "نوبت"
        verbose_name_plural = "نوبت‌ها"

    def __str__(self):
        return f"{self.full_name} - {self.doctor.name} ({self.date} {self.time})"

# ۴. مدل‌های وبلاگ
class BlogCategory(models.Model):
    title = models.CharField(max_length=100, verbose_name="عنوان دسته")
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = "دسته‌بندی مقالات"
        verbose_name_plural = "دسته‌بندی‌های مقالات"

    def __str__(self):
        return self.title

class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name="عنوان مقاله")
    slug = models.SlugField(unique=True, blank=True)
    category = models.ForeignKey(BlogCategory, on_delete=models.SET_NULL, null=True, related_name='posts', verbose_name="دسته بندی")
    content = models.TextField(verbose_name="متن مقاله")
    summary = models.TextField(verbose_name="خلاصه برای پیش‌نمایش")
    image = models.ImageField(upload_to='blog/', verbose_name="تصویر شاخص")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ انتشار")
    updated_at = models.DateTimeField(auto_now=True)
    view_count = models.PositiveIntegerField(default=0, verbose_name="تعداد بازدید")

    class Meta:
        verbose_name = "مقاله"
        verbose_name_plural = "مقالات"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

# ۵. مدل‌های گالری
class GalleryCategory(models.Model):
    title = models.CharField(max_length=100, verbose_name="نام دسته بندی (مثلا جراحی بینی)")
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = "دسته بندی گالری"
        verbose_name_plural = "دسته بندی‌های گالری"

    def __str__(self):
        return self.title

class GalleryItem(models.Model):
    category = models.ForeignKey(GalleryCategory, on_delete=models.CASCADE, related_name='items', verbose_name="دسته بندی")
    title = models.CharField(max_length=200, verbose_name="عنوان نمونه کار")
    before_image = models.ImageField(upload_to='gallery/before/', verbose_name="تصویر قبل")
    after_image = models.ImageField(upload_to='gallery/after/', verbose_name="تصویر بعد")
    description = models.TextField(blank=True, verbose_name="توضیحات کوتاه")

    class Meta:
        verbose_name = "نمونه کار"
        verbose_name_plural = "گالری نمونه کارها"

    def __str__(self):
        return f"{self.category.title} - {self.title}"