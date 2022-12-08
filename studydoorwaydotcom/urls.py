
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from rest_framework import routers
from .views import home,about_us_view
from chat.views import getMessages
from rest_framework import routers
from accounts.views import (
	login_view,
	register_view,
	logout_view,
	userprofile_view,
    register_as_teacher_view,
)
router=routers.DefaultRouter()
router.register(r'ajaxusers',getMessages)

app_name = 'ratings'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('classes.urls')),
    path('', include('internetforum.urls')),
    path('', include('quizes.urls',namespace='quizes')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('',home,name='home'),
    path('about_us/',about_us_view,name='about_us'),
    path('accounts/login/', login_view,name='login'),
    path('accounts/signup/', register_view,name='signup'),
    path('accounts/logout/', logout_view,name='logout'),
    path('accounts/userprofile/<int:profile_id>', userprofile_view,name='userprofile'),
    path('accounts/register_as_teacher/<int:prof_id>', register_as_teacher_view,name='register_as_teacher'),
    path('chat/', include('chat.urls', namespace='chat')),
    path('ratings/', include('star_ratings.urls', namespace='ratings')),
    
]
urlpatterns+=router.urls
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)