
from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
import notifications.urls

urlpatterns = [
    path('dadmin/', admin.site.urls),
    path('', include('qrmenu.urls')),
    path('admin/', include('qradmin.urls')),
    path('accounts/', include('accounts.urls')),
    path('payments/', include('payments.urls')),
    url('^inbox/notifications/', include(notifications.urls, namespace='notifications')),
    url(r'^currencies/', include('currencies.urls'))
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
