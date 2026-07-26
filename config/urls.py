from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from allauth.account.views import ConfirmEmailView
from django.conf import settings
from django.conf.urls.static import static
from apps.accounts.views import CustomLoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path("accounts/", include("allauth.urls")), 
    path("api/auth/login/", CustomLoginView.as_view(), name="rest_login"),
    path('api/auth/', include('dj_rest_auth.urls')),
    path("api/auth/registration/account-confirm-email/<str:key>/", ConfirmEmailView.as_view(), name="account_confirm_email"),
    path('api/auth/registration/', include('dj_rest_auth.registration.urls')),
    
    # API schema and documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    