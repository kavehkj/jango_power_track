from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView ,DetailView
from .models import Device , DeviceData
from django.db.models import Q




class home(ListView, LoginRequiredMixin):
    template_name = 'track/home.html'
    model = Device
    context_object_name = 'devices'


    def get_queryset(self):
        return Device.objects.filter(users=self.request.user)

class login(LoginView):
    template_name = 'track/login.html'
    next_page = reverse_lazy('home')

class logout(LogoutView):
    next_page = reverse_lazy('home')




class search_view(ListView):
    model = Device  
    template_name = 'track/home.html'
    context_object_name = 'devices' 


    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
 
            return Device.objects.filter(
                Q(id__icontains=query) |  
                Q(name__icontains=query) |
                Q(location__icontains=query)
            )
        return Device.objects.none()  

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q')
        return context




class device_details(DetailView):
    model = Device  
    template_name = 'track/device_details.html'  
    context_object_name = 'device' 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        latest_device_data = DeviceData.objects.filter(device_id_data=self.object).order_by('-times').first()
        context['latest_device_data'] = latest_device_data
        
        if latest_device_data:
            if latest_device_data.voltage > 120 and latest_device_data.voltage < 240:
                status = "normal"
            else:
                status = "abnormal"
        else:
            status = "unknown"  
        
        context['status'] = status

        device_data = DeviceData.objects.filter(device_id_data=self.object).order_by('times')
 
        context['times'] = [data.jalali_times for data in device_data]
        context['voltages'] = [float(data.voltage) for data in device_data]  
        context['currents'] = [float(data.current) for data in device_data]
        context['temperatures'] = [float(data.temperature) for data in device_data]
 
        return context