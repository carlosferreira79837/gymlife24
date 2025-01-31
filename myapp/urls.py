from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from .views import calorie_calculator, home, exercises, register, profil, saved_exercises, toggle_save_exercise, suggest_exercise, suggest

urlpatterns = [
    path('', home, name='home'),
    path('calorie_calculator', calorie_calculator, name='calorie_calculator'),
    path('exercises', exercises, name='exercises'),
    path('register/', register, name='register'),
    path('profil', profil, name='profil'),
    path('saved_exercises', saved_exercises, name='saved_exercises'),
    path('save-exercise/<int:exercise_id>/', toggle_save_exercise, name='toggle_save_exercise'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('suggest', suggest, name='suggest'),
    path('suggest_exercise', suggest_exercise, name='suggest_exercise')
]