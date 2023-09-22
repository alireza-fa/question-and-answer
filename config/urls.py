from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView


docs_urls = [
    path('api/', include(([
        path('schema/', SpectacularAPIView.as_view(), name='schema'),
        path('schema/swagger/', SpectacularSwaggerView.as_view(), name='swagger'),
        path('schema/redoc/', SpectacularRedocView.as_view(), name='redoc'),
    ]))),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(([
        path('accounts/', include('accounts.urls')),
        path('jwt/', include('jwt_authenticate.urls')),
    ]))),
] + docs_urls


admin.site.site_header = "Q&A Admin"
admin.site.site_title = "Q&A Admin Portal"
admin.site.index_title = "Welcome to Q&A"
