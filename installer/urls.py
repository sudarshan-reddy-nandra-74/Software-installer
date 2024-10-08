from django.urls import path
from .views import index, install_software

urlpatterns = [
    path('', index, name='index'),  # Renders the form
    path('install/', install_software, name='install_software'),  # Handles form submission
]
