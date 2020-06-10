from django.urls import path, re_path, include
import consent_log.urls

urlpatterns =[
    path("consent_log/", include("consent_log.urls"))
]
