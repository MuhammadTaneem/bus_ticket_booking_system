from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('auth/', include('tauth.urls')),
    path('buses/', include('bus.urls')),
    path('schedule/', include('schedule.urls')),
    path('route/', include('route.urls')),
    path('reservation/', include('ticket_reservation.urls')),
    # path('schedule/', include('schedule.urls')),

]
urlpatterns += static(settings.MEDIA_URL,
                      document_root=settings.MEDIA_ROOT)
