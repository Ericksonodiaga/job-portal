from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('jobosoft.urls')),
    path('', include('accounts.urls')),
    path("social-auth/", include("social_django.urls", namespace="social")),


]

