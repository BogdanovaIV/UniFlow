from django.core.exceptions import ValidationError
from django.db import models

# Create your models here.
class StudyGroup(models.Model):
    """
    Represents a study group.

    Attributes:
        name (str): The name of the study group, unique within the database.
        active (bool): Indicates whether the study group is currently active.
        Defaults to True.

    Meta:
        ordering (list): The default ordering of StudyGroup instances
        is by name.
    """
    name = models.CharField(max_length=100, unique=True, null=False)
    active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ["name"]

    def __str__(self):
        """
        Returns the string representation of the StudyGroup instance.

        Returns:
            str: The name of the study group.
        """
        return self.name


class Term(models.Model):
    """
    Represents an academic term with a start and end date.

    Attributes:
        name (str): The name of the term, unique within the database.
        date_from (date): The start date of the term, must be unique
        and cannot be null.
        date_to (date): The end date of the term, must be unique
        and cannot be null.
        active (bool): Indicates whether the term is currently active.
        Defaults to True.

    Meta:
        ordering (list): The default ordering of Term instances is by date_from.
        constraints (list): Enforces uniqueness of date_from
        and date_to fields together.
    """
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
        """
        Validates the Term instance before saving.

        Raises:
            ValidationError: If date_from is not earlier than date_to
            or if there are overlapping terms.
        """
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
        """
        Returns the string representation of the Term instance.

        Returns:
            str: A formatted string containing the name
            and date range of the term.
        """
        return f"{self.name} - ({self.date_from}-{self.date_to})"


class Subject(models.Model):
    """
    Represents a subject.

    Attributes:
        name (str): The name of the subject, unique within the database.
        active (bool): Indicates whether the subject is currently active.
        Defaults to True.

    Meta:
        ordering (list): The default ordering of Subject instances
        is by name.
    """
    name = models.CharField(max_length=100, unique=True, null=False)
    active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ["name"]

    def __str__(self):
        """
        Returns the string representation of the Subject instance.

        Returns:
            str: The name of the subject.
        """
        return self.name