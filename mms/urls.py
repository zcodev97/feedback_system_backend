from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from mms_api.apiviews import (
    FeedBackAPI, CreateFeedBackAPI, FeedBackReportAPI)
from core.serializers import CustomUserSerializer
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from rest_framework.authtoken import views
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        # Assuming you have a serializer for your user model
        user_serializer = CustomUserSerializer(self.user).data
        data.update({'user': user_serializer})
        return data


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


# Admin Site Config
admin.sites.AdminSite.site_header = 'دار السلطاني'
admin.sites.AdminSite.site_title = 'دار السلطاني'
admin.sites.AdminSite.index_title = 'دار السلطاني'

urlpatterns = [
    path('admin/', admin.site.urls),
    # YOUR PATTERNS
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('api/schema/swagger-ui/',
         SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/',
         SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    # mms api
    # all vendors
    path('feedbacks/', FeedBackAPI.as_view(), name="all feedbacks"),
    path('create_feedback/', CreateFeedBackAPI.as_view(),
         name="create feedback api"),
    path('report_feedback/', FeedBackReportAPI.as_view(),
         name="report feedback api"),

    # login
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]
# Configure URL patterns for serving media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
