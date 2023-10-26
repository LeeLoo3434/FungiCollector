from django.urls import path
from . import views
from .views import FungiNoteCreate
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.home, name='home'),
    path('fungi/', views.FungiList.as_view(), name='index'),
    path('fungi/create/', views.FungiCreate.as_view(), name='fungi_create'),
    path('fungi/<int:pk>/', views.FungiDetail.as_view(), name='fungi_detail'),
    path('fungi/<int:pk>/update/', views.FungiUpdate.as_view(), name='fungi_update'),
    path('fungi/<int:pk>/delete/', views.FungiDelete.as_view(), name='fungi_delete'),
    path('about/', views.about, name='about'),
    path('accounts/signup/', views.signup, name='signup'),
    path('fungi/<int:fungi_id>/notes/', views.FungiNoteCreate.as_view(), name='fungi_notes'),
    path('fungi/<int:fungi_id>/note/create/', FungiNoteCreate.as_view(), name='funginote_create'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
