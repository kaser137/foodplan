from django.urls import path
from users.views import login, registration

app_name = 'users'

urlpatterns = [
    path('auth/', login, name='login'),
    path('registration/', registration, name='registration'),

]