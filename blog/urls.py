from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/',include('blog_app.urls')),
    path('auth/',include('authen.urls')),
]
