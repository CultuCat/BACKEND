"""
URL configuration for cultucat project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from scripts.views import scr_refresh

schema_view = get_schema_view(
   openapi.Info(
      title="CultuCat API",
      default_version='v1',
      description="Tota la cultura al teu abast",
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('events/', include('events.urls'), name='Esdeveniments'),
    path('tickets/', include('ticket.urls'), name='Tickets'),
    path('comments/', include('comment.urls'), name='Comments'),
    path('docswagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('spaces/', include('spaces.urls'), name='Espais'),
    path('users/', include('user.urls'), name='Usuaris'),
    path('refresh/', scr_refresh, name='Refresh'),
    path('trophies/', include('trophy.urls'), name='Trophies'),
    path('verificar_discount/', include('discount.urls'), name='Discounts'),
]
