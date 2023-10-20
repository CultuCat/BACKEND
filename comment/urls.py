from rest_framework import routers
from . import views
from django.urls import path

# router = routers.DefaultRouter()
# router.register(r'', views.CommentsView, basename='comments')

# urlpatterns = router.urls

urlpatterns = [
    path('post_comment/', views.post_comment, name='post_comment'),
    path('get_comments/<int:event_id>/', views.get_comments_for_event, name='get_comments_for_event'),
]