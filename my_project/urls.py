
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from allauth.account.views import LoginView



from django.conf.urls import handler404
from lms.views import handler404 as custom_handler404


handler404 = custom_handler404


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('lms.urls')),
    path('accounts/', include('allauth.urls')),
    path('accounts/profile/', RedirectView.as_view(url='/'), name='profile_redirect'),
    path('accounts/login/', LoginView.as_view(), name='account_login'),
   
 





]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)