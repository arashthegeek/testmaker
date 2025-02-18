from django.db import models

# Create your models here.

class IdCourse(models.Model):
    id = models.CharField(max_length=8, primary_key=True)
    course = models.CharField(max_length=255)
    
    def __str__(self):
        return f"{self.id}"

class IdQuastion(models.Model):
    id = models.IntegerField(primary_key=True)
    IdCoursef = models.ForeignKey(IdCourse,on_delete=models.CASCADE)
    Quastion = models.CharField(max_length=60)
    Option_a = models.CharField(max_length=50)
    Option_b = models.CharField(max_length=50)
    Option_c = models.CharField(max_length=50)
    Option_d = models.CharField(max_length=50)
    Correct_Option = models.CharField(max_length=1)
    
    def __str__(self):
        return f"{self.IdCoursef}"