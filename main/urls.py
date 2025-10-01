from django.urls import path
from . import views

urlpatterns = [
    path("", views.scan_dashboard, name="scan_dashboard"),
    path("submit/", views.submit_code, name="submit_code"),
]
