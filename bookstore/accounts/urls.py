from django.urls import path
from .views import *

urlpatterns = [
path('login/', login_user, name='login'),   
path('logout/', logout_user, name='logout'),
path('register/', register_user, name='register'),
path('profile/', profile_user, name='profile'),
path('edit_profile/', edit_profile, name='edit_profile'),
path('change_password/', change_password, name='change_password'),
path('contact/', contact_detail, name='contact_detail'),
path('about/', about_detail, name='about_detail'),
]
