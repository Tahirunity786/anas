
from django.urls import path
from core.views import Engine

urlpatterns = [
    path('engine', Engine.as_view(), name="Engine")
]
