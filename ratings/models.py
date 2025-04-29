from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator

class Module(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.code} {self.name}"

class Professor(models.Model):
    professor_id = models.CharField(max_length=10, unique=True)
    name = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(2)]
    )

    def __str__(self):
        return f"{self.professor_id}, {self.name}"

class ModuleInstance(models.Model):
    SEMESTER_CHOICES = (
        (1, 'Semester 1'),
        (2, 'Semester 2'),
    )

    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    year = models.IntegerField()
    semester = models.IntegerField(choices=SEMESTER_CHOICES)
    professors = models.ManyToManyField(Professor)

    def __str__(self):
        return f"{self.module.code} {self.year} Semester {self.semester}"

from django.core.validators import MinValueValidator, MaxValueValidator

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    module_instance = models.ForeignKey(ModuleInstance, on_delete=models.CASCADE)
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

    class Meta:
        unique_together = ('user', 'professor', 'module_instance')

    def __str__(self):
        return f"{self.user.username} rated {self.professor.name} in {self.module_instance} : {self.rating}"

