from django.urls import path
from users.views import login, registration, profile, logout

app_name = 'users'

urlpatterns = [
    path('auth/', login, name='login'),
    path('registration/', registration, name='registration'),
    path('lk/', profile, name='profile'),
    path('logout/', logout, name='logout'),
]