from django.contrib import admin
from django.urls import path, include
from tasks import urls as urls_tasks

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('tasks/', include(urls_tasks))
]
