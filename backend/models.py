from django.db import models

class Employee(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    date = models.DateField()
    jsonData = models.TextField()
    def __str__(self):
        return self.name