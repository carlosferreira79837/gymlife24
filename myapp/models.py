from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class MuscleGroup(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
class Exercise(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    gif = models.ImageField(upload_to='exercise_gifs/', null=True, blank=True)
    muscle_group = models.ForeignKey(MuscleGroup, related_name="exersices", on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name


class SavedExercise(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    #saved_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.exercise.name}"