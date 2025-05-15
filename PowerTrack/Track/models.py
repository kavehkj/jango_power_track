from django.db import models
import jdatetime  
from datetime import datetime 
from django.utils.text import slugify
from django.contrib.auth.models import User

class Device(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    jalali_created_at = models.CharField(max_length=100 , blank=True)
    slug = models.SlugField(blank=True, null=True)
    users = models.ManyToManyField(User, related_name="devices") 

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)  
        super().save(*args, **kwargs)


        if self.created_at is None:
            self.created_at = datetime.now()

        jalali_created = jdatetime.datetime.fromgregorian(datetime=self.created_at)
        self.jalali_created_at = jalali_created.strftime('%Y/%m/%d %H:%M:%S')
        super().save(*args, **kwargs) 


class DeviceData(models.Model):
    device_id_data = models.ForeignKey(Device, on_delete=models.CASCADE)
    voltage = models.FloatField()
    current = models.FloatField()
    temperature = models.FloatField()
    times = models.DateTimeField(auto_now_add=True)
    jalali_times = models.CharField(max_length=20, blank=True) 

    def __str__(self):
        return str(self.device_id_data) + ' - ' + str(self.jalali_times)

    def save(self, *args, **kwargs):
        if self.times is None:
            self.times = datetime.now()


        jalali_date = jdatetime.datetime.fromgregorian(datetime=self.times)
        self.jalali_times = jalali_date.strftime('%Y/%m/%d %H:%M:%S')
        super().save(*args, **kwargs) 



        