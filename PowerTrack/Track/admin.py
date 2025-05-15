from django.contrib import admin
from .models import Device, DeviceData
from django.contrib.auth.models import User

# فیلتر سفارشی برای فیلتر کردن دستگاه‌ها بر اساس کاربر
class UserFilter(admin.SimpleListFilter):
    title = 'User'  # عنوان فیلتر
    parameter_name = 'user'  # پارامتر URL برای فیلتر

    def lookups(self, request, model_admin):
        # لیست کاربران برای نمایش در فیلتر
        users = User.objects.all()
        return [(user.id, user.username) for user in users]

    def queryset(self, request, queryset):
        # اعمال فیلتر بر اساس کاربر انتخاب‌شده
        if self.value():
            return queryset.filter(users__id=self.value())
        return queryset

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    # فیلدهایی که در لیست دستگاه‌ها نمایش داده می‌شوند
    list_display = ('name', 'location', 'created_at', 'jalali_created_at', 'display_users', 'slug')
    
    # امکان جستجو بر اساس نام دستگاه و مکان
    search_fields = ('name', 'location','users__username')
    
    # فیلترها برای مرتب‌سازی بر اساس تاریخ ایجاد، مکان و کاربر
    list_filter = ('created_at', 'location', UserFilter)  # اضافه کردن فیلتر سفارشی
    
    # امکان انتخاب کاربران به‌صورت افقی (برای رابط کاربری بهتر)
    filter_horizontal = ('users',)
    
    # نمایش خودکار اسلاگ در صورت خالی بودن
    prepopulated_fields = {'slug': ('name',)}
    
    # تابع برای نمایش کاربران به‌صورت رشته‌ای
    def display_users(self, obj):
        return ", ".join([user.username for user in obj.users.all()])
    
    display_users.short_description = 'Users'  # عنوان ستون در لیست دستگاه‌ها

@admin.register(DeviceData)
class DeviceDataAdmin(admin.ModelAdmin):
    # فیلدهایی که در لیست داده‌های دستگاه نمایش داده می‌شوند
    list_display = ('device_id_data', 'voltage', 'current', 'times', 'jalali_times')
    
    # امکان جستجو بر اساس دستگاه مرتبط
    search_fields = ('device_id_data__name',)
    
    # فیلترها برای مرتب‌سازی بر اساس زمان و دستگاه
    list_filter = ('times', 'device_id_data')
    
    # نمایش زمان به‌صورت Jalali در لیست
    def jalali_times_display(self, obj):
        return obj.jalali_times
    
    jalali_times_display.short_description = 'Jalali Times'  # عنوان ستون در لیست داده‌ها