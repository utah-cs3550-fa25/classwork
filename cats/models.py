from django.db import models

# Create your models here.

class Cat(models.Model):
    name = models.CharField(
        max_length=20,
        blank=True)
    age = models.IntegerField(
        null=True, blank=True)
    breed = models.CharField(
        max_length=30,
        blank=True)
    photo = models.ImageField(
        null=True, blank=True)

    color = models.CharField(max_length=10)
    backstory = models.TextField(
        blank=True)
    gender = models.CharField(max_length=10)
    weight_lbs = models.FloatField()

    health = models.OneToOneField(
        'HealthRecord', on_delete=models.RESTRICT)

    def adoptability(self):
        # ...
        return 100



class HealthRecord(models.Model):
    spayed_neutered = models.BooleanField()

class Vaccination(models.Model):
    patient = models.ForeignKey('Cat', on_delete=models.CASCADE)

class Illness(models.Model):
    patient = models.ForeignKey('Cat', on_delete=models.CASCADE)
    type = models.CharField(max_length=200)
    more = models.TextField(blank=True)
