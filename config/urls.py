from django.contrib import admin
from django.urls import path, include

from apps.ratings.views import rate_object_view
from apps.users import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('jet/', include('jet.urls', 'jet')),
    path('admin/', admin.site.urls),
    path('', views.home),
    path('__debug__/', include('debug_toolbar.urls')),
    path('users/', include('apps.users.urls')),
    path('customer/', include('apps.customer.urls')),
    path('courier/', include('apps.courier.urls')),
    path('object-rate/', rate_object_view)
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
