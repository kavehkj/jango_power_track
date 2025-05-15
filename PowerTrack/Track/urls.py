from django.urls import path
from .views import home ,device_details ,login,logout ,search_view


urlpatterns = [
    path('', home.as_view(), name='home'),
    path('login/', login.as_view(), name='login'),
    path('logout/', logout.as_view(), name='logout'),
    path('device_details/<slug:slug>', device_details.as_view(), name='device_details'),
    path('search/', search_view.as_view(), name='search'),
    
]
