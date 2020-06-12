from django.urls import path, re_path, include
from .apps import app_name
from .views import ConfirmView, RejectView

urlpatterns = [
    path("confirm/<str:token>", ConfirmView.as_view(), name="confirm"),
    path("reject/<str:token>", RejectView.as_view(), name="reject"),
]
