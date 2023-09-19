from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

from users.views import login, register

urlpatterns = [
    path('register/',register,name='register'),
    path('login/',login,name='login'),
    path('',include('concertconnect.urls')),

]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)

