from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Admin site
    path('admin/', admin.site.urls),

    # All the smartbin app’s URLs live under “/”
    path('', include('smartbin.urls')),
]
