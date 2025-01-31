from django.shortcuts import render, HttpResponse, redirect
from .models import Exercise, MuscleGroup, SavedExercise
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.
def calorie_calculator(request):
    result = None
    bmr = None
    bedarf = None
    if request.method == 'POST':
        age = int(request.POST.get('age'))
        weight = float(request.POST.get('weight'))
        height = float(request.POST.get('height'))
        gender = request.POST.get('gender')
        activity = float(request.POST.get('activity'))
        
        # Mifflin-St Jeor Formel
        if gender == 'male':
            bmr = 10 * weight + 6.25 * height - 5 * age + 5
        else:
            bmr = 10 * weight + 6.25 * height - 5 * age - 161

        bedarf = bmr * activity
        
    return render(request, 'calculator.html', {'bedarf': bedarf,
                                               'bmr': bmr})
        
def home(request):
    return render(request, 'home.html')

def exercises(request):
    muscle_groups = MuscleGroup.objects.all()
    exercises = Exercise.objects.all()
    saved_exercises = None
    if 'muscle_group' in request.GET:
        if request.GET['muscle_group'] == "favorites" and request.user.is_authenticated:
            sa = SavedExercise.objects.filter(user=request.user)
            exercises = [saved.exercise for saved in sa]
        elif request.GET['muscle_group'] == "favorites" and not request.user.is_authenticated:
            return redirect('login')
        elif request.GET['muscle_group'] != "":
            selected_muscle_group_id = request.GET['muscle_group']
            exercises = exercises.filter(muscle_group_id=selected_muscle_group_id)
    if request.user.is_authenticated:
        saved_exercises = SavedExercise.objects.filter(user=request.user).values_list('exercise', flat=True)
    
    return render(request, 'exercises.html', {'exercises': exercises,
                                              'muscle_groups': muscle_groups,
                                              'saved_exercises': saved_exercises})
    
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account für {username} wurde erstellt! Du kannst dich jetzt anmelden.')
            return redirect('login')
    else:
        form = UserCreationForm()
        
    return render(request, 'register.html', {'form': form})

@login_required
def profil(request):
    return render(request, 'profil.html')

def saved_exercises(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    saved_exercises = SavedExercise.objects.filter(user=request.user)
    return render(request, 'saved_exercises.html', {'saved_exercises': saved_exercises})


def toggle_save_exercise(request, exercise_id):
    if not request.user.is_authenticated:
        print("hallo")
        return JsonResponse({'error': 'Not authenticated', 'message': 'Bitte logge dich ein, um diese Aktion auszuführen.'}, status=401)
    
    exercise = get_object_or_404(Exercise, id=exercise_id)
    saved_exercise, created = SavedExercise.objects.get_or_create(user=request.user, exercise=exercise)

    if not created:
        saved_exercise.delete()
        return JsonResponse({'saved': False, 'message': 'Exercise removed from saved list'})
    
    return JsonResponse({'saved': True})

def suggest(request):
    return render(request, 'suggest.html')

def suggest_exercise(request):
    if request.method == 'POST':
        name = request.POST.get('exercise_name')
        description = request.POST.get('description')
        
        send_mail(
            subject="Neue Übung vorgeschlagen",
            message=f"Name: {name}\n\nBeschreibung: {description}",
            from_email='carlosferreirapacheco732@gmail.com',
            recipient_list=["carlos2009@live.de"],
        )
        return redirect('exercises')
    
    return JsonResponse({'message': 'Ungültige Anfrage'}, status=400)
        