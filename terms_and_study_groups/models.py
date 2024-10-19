from django.core.exceptions import ValidationError
from django.db import models

# Create your models here.
class StudyGroup(models.Model):
    name = models.CharField(max_length=100, unique=True, null=False)
    active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Term(models.Model):
    name = models.CharField(max_length=100, unique=True, null=False)
    date_from = models.DateField(unique=True, null=False)
    date_to = models.DateField(unique=True, null=False)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ["date_from"]

        constraints = [
            models.UniqueConstraint(
                fields=['date_from', 'date_to'], name='unique_term_dates'
            ),
        ]

    def clean(self):
        # Check if date_from is less than date_to
        if self.date_from >= self.date_to:
            raise ValidationError(
                "The start date must be earlier than the end date."
            )

        # Check for overlapping periods
        overlapping_terms = Term.objects.filter(
            active=True,  # Check only active terms
            date_from__lt=self.date_to,
            date_to__gt=self.date_from
        )
        if overlapping_terms.exists():
            raise ValidationError(
                "This term overlaps with an existing term."
            )

    def __str__(self):
        return f"{self.name} - ({self.date_from}-{self.date_to})"