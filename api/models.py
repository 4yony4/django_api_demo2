from django.db import models

# Create your models here.
class Item(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
    

class Persona(models.Model):
    name = models.CharField(max_length=255)
    edad = models.IntegerField()
    altura = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name