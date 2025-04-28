from django.urls import path
from users import views  # Correct import from the cars app

app_name = "users"

urlpatterns = [
    path('login/', views.login, name="login"),
    path('registration/', views.registration, name="registration"),
    path('profile/', views.profile, name="profile"),
    path('logout/', views.logout, name="logout"),
]
