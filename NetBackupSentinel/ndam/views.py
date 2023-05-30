from typing import Any, Dict
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView
from ajax_datatable.views import AjaxDatatableView
from ndam.models import Device
from django.views.generic.edit import CreateView
from ndam.forms import DeviceForm
from django_htmx.http import HttpResponseClientRefresh


# Create your views here.
class DeviceHomeView(TemplateView):
    template_name = "device/home.html"


class DeviceAjaxView(AjaxDatatableView):
    model = Device
    title = "Device"
    initial_order = [
        ["created_at", "desc"],
    ]

    length_menu = [[10, 20, 50, 100, -1], [10, 20, 50, 100, "all"]]
    search_values_separator = "+"

    column_defs = [
        {"name": "name", "visible": True, "title": "Name"},
        {"name": "ip_address", "visible": True, "title": "IP Address"},
        {"name": "port", "visible": True, "title": "Port"},
        {"name": "connection_type", "visible": True, "title": "Connection Type"},
        {"name": "modul_type", "visible": True, "title": "Modul Type"},
        {"name": "created_at", "visible": True, "title": "Created At"},
    ]


class DeviceCreateView(CreateView):
    model = Device
    form_class = DeviceForm
    template_name = "device/create.html"
    success_url = reverse_lazy("ndam:device_home")

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["title"] = "Create Device"
        context["url"] = reverse("ndam:device_create")
        return context

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        super().form_valid(form)
        return HttpResponseClientRefresh()
