from django.urls import path
from ndam import views

app_name = "ndam"


urlpatterns = [
    path("devices/", views.DeviceHomeView.as_view(), name="device_home"),
    path("devices/ajax", views.DeviceAjaxView.as_view(), name="device_ajax"),
    path("devices/create", views.DeviceCreateView.as_view(), name="device_create"),
]
