from django.db import models

# Create your models here.
class StudyGroup(models.Model):
    name = models.CharField(max_length=100, unique=True)
    active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ["name"]
        
    def __str__(self):
        return self.name