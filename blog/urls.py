from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from .views import *

app_name = 'blog'

urlpatterns = [
    # path('', views.home, name='home'),
    # path('articles/', views.articles, name='articles'),
    # path('<slug:article>/', views.article, name='article'),
    
    path('home/', home, name='home'),
    path('create-profile/', create_profile, name='create_profile'),
    path('add-property/', add_property, name='add_property'),
    path('', profile_list, name='profile_list'),
    path("property_list/", property_list, name="property_list"),
    path('profile_details/<int:property_id>/<str:persontype>/', view_profile_details, name='view_profile_details'),
    path('edit_property/<int:property_id>/<str:persontype>/', views.edit_property, name='edit_property'),

    path('delete_property/<int:property_id>/<str:persontype>/', views.delete_property, name='delete_property'),
    path('crm_details/<int:property_id>/', crm_details, name='crm_details'),        


    path("user_login",user_login,name="user_login"),
    path("signup/", sign_up, name="sign_up"),
    path("logout/", user_logout, name="log_out"),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)