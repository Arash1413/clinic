from django.db import models
from django.utils.text import slugify
from django.db import models
from django.urls import reverse
# مدل خدمات (مثلاً لیزر، بوتاکس و ...)
class Service(models.Model):
    title = models.CharField(max_length=200, verbose_name="نام خدمت (مثلاً کراتین مو)")
    image = models.ImageField(upload_to='services/', verbose_name="تصویر خدمت")
    slug = models.SlugField(unique=True, verbose_name="شناسه در آدرس (انگلیسی)")
    description = models.TextField(verbose_name="توضیحات کامل خدمت")

    def __str__(self):
        return self.title

    # این متد کمک می‌کند وقتی روی کارت کلیک شد به صفحه جزئیات برود
    def get_absolute_url(self):
        return reverse('service_detail', kwargs={'slug': self.slug})

# مدل وبلاگ
class Post(models.Model):
    title = models.CharField(max_length=200)
    summary = models.TextField()
    body = models.TextField()
    image = models.ImageField(upload_to='blog/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# مدل نوبت‌دهی ساده
class Appointment(models.Model):
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    date = models.DateField()
    message = models.TextField(blank=True)

    def __str__(self):
        return f"{self.full_name} - {self.service}"



# این‌ها را به انتهای فایل models.py اضافه کنید

class GalleryCategory(models.Model):
    title = models.CharField(max_length=100, verbose_name="نام دسته بندی (مثلا جراحی بینی)")
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = "دسته بندی‌های گالری"

    def __str__(self):
        return self.title

class GalleryItem(models.Model):
    category = models.ForeignKey(GalleryCategory, on_delete=models.CASCADE, related_name='items')
    title = models.CharField(max_length=200, verbose_name="عنوان نمونه کار")
    before_image = models.ImageField(upload_to='gallery/before/', verbose_name="تصویر قبل")
    after_image = models.ImageField(upload_to='gallery/after/', verbose_name="تصویر بعد")
    description = models.TextField(blank=True, verbose_name="توضیحات کوتاه")

    def __str__(self):
        return f"{self.category.title} - {self.title}"
    

class BlogCategory(models.Model):
    title = models.CharField(max_length=100, verbose_name="عنوان دسته")
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = "دسته‌بندی مقالات"

    def __str__(self):
        return self.title

class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name="عنوان مقاله")
    slug = models.SlugField(unique=True, blank=True)
    category = models.ForeignKey(BlogCategory, on_delete=models.SET_NULL, null=True, related_name='posts')
    content = models.TextField(verbose_name="متن مقاله")
    summary = models.TextField(verbose_name="خلاصه برای پیش‌نمایش")
    image = models.ImageField(upload_to='blog/', verbose_name="تصویر شاخص")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    view_count = models.PositiveIntegerField(default=0) # برای نمایش تعداد بازدید

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Appointment(models.Model):
    # انتخاب ساعت‌های کاری (مثلاً هر نیم ساعت یک نوبت)
    TIME_CHOICES = [
        ('10:00', '10:00'), ('10:30', '10:30'),
        ('11:00', '11:00'), ('11:30', '11:30'),
        ('16:00', '16:00'), ('16:30', '16:30'),
        ('17:00', '17:00'), ('17:30', '17:30'),
        ('18:00', '18:00'), ('18:30', '18:30'),
    ]

    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.CharField(max_length=5, choices=TIME_CHOICES) # فیلد جدید ساعت
    message = models.TextField(blank=True)

    class Meta:
        # جلوگیری از ثبت نوبت تکراری (یک تاریخ و یک ساعت خاص فقط یکبار رزرو شود)
        unique_together = ('date', 'time')

    def __str__(self):
        return f"{self.full_name} - {self.date} {self.time}"




# Create your models here.
