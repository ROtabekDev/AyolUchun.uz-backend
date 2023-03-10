from django.db import models

from helpers.models import BaseModel
from helpers.utils import get_timer

from mutagen.mp4 import MP4, MP4StreamInfoError


class Category_for_course(BaseModel):
    """Kurslar uchun kategoriya"""
    title = models.CharField('Sarlavhasi', max_length=150)
    slug = models.SlugField('Slugi', max_length=150)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Kategoriya'
        verbose_name_plural = 'Kategoriyalar'


class Course(BaseModel):
    """Kurslar uchun model"""

    COURSE_TYPE = (
        ('Bestseller', 'Ko`p sotilgan'),
        ('Recommended', 'Tavsiya etiladi'),
        ('Nothing', 'Oddiy'),
    )

    title = models.CharField('Kurs nomi', max_length=150)
    slug = models.SlugField('Slugi', max_length=150)
    category_id = models.ForeignKey(Category_for_course, on_delete=models.CASCADE)
    desciption = models.TextField('Kurs haqida ma`lumot')
    slider = models.ImageField('Rasm', upload_to='course/course/slider/')
    author = models.CharField('Muallif', max_length=150)
    type = models.CharField('Kurs turi', choices=COURSE_TYPE, max_length=15, default='Nothing')
    price = models.DecimalField('Narxi', max_digits=12, decimal_places=2)
    is_discount = models.BooleanField('Chegirma', default=False)
    discount_price = models.DecimalField('Chegirmadagi narxi', max_digits=12, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Kurs'
        verbose_name_plural = 'Kurslar'


class Section(BaseModel):
    """Bo`limlar uchun model"""

    SECTION_TYPE = (
        ('Not seen', 'Ko`rilmagan'),
        ('In progress', 'Jarayonda'),
        ('Reviewed', 'Ko`rilgan'),
    )

    section_title = models.CharField('Sarlavhasi', max_length=150)
    section_number = models.PositiveIntegerField('Tartib nomeri', default=1)
    section_type = models.CharField('Bo`lim turi', choices=SECTION_TYPE, default='Not seen', max_length=20)
    is_public = models.BooleanField(default=False)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Bo`lim'
        verbose_name_plural = 'Bo`limlar'

class Episode(BaseModel):
    """Videolar uchun model"""
    title = models.CharField('Nomi', max_length=150)
    file = models.FileField('Fayl', upload_to='course/episode/file/')
    length = models.DecimalField(max_digits=100,decimal_places=2, blank=True, null=True)
    section_id = models.ForeignKey(Section, on_delete=models.CASCADE, blank=True, null=True)

    def get_video_length(self):
        try:
            video=MP4(self.file)
            return video.info.length
            
        except MP4StreamInfoError:
            return 0.0

    def get_video_length_time(self):
        return get_timer(self.length)
    
    def get_video(self):
        return self.file.path
    
    def save(self,*args, **kwargs):
        self.length=self.get_video_length()
        print(self.length)
        print(self.file.path)
        print(self.get_video_length_time()) 

        return super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Epizod'
        verbose_name_plural = 'Epizodlar'