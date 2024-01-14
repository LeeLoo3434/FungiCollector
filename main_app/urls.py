from django.urls import path
from . import views
from .views import CommentCreate, CommentUpdate, CommentDelete
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('fungi/', views.FungiList.as_view(), name='index'),
    path('fungi/create/', views.FungiCreate.as_view(), name='fungi_create'),
    path('fungi/<int:pk>/', views.FungiDetail.as_view(), name='fungi_detail'),
    path('fungi/<int:pk>/update/', views.FungiUpdate.as_view(), name='fungi_update'),
    path('fungi/<int:pk>/delete/', views.FungiDelete.as_view(), name='fungi_delete'),
    path('fungi/<int:fungi_id>/like/', views.like_fungi, name='like_fungi'),
    path('about/', views.about, name='about'),
    path('accounts/signup/', views.signup, name='signup'),
    path('profile/<int:user_id>/', views.profile_page, name='profile_page'),  # New URL for profile_page
    path('userfeed/', views.UserFeed.as_view(), name='user_feed'),  # New URL for UserFeed

    # Comment related URLs
    path('fungi/<int:fungi_id>/comment/create/', views.CommentCreate.as_view(), name='comment_create'),  # Updated this line
    path('fungi/<int:fungi_id>/comment/<int:pk>/update/', CommentUpdate.as_view(), name='comment_update'),
    path('fungi/<int:fungi_id>/comment/<int:pk>/delete/', CommentDelete.as_view(), name='comment_delete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
