from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
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

class WeekdayChoices(models.IntegerChoices):
    """
    Enumeration for days of the week.

    Each day is represented by an integer value corresponding to its order
    in the week.
    """
    MONDAY = 0, 'Monday'
    TUESDAY = 1, 'Tuesday'
    WEDNESDAY = 2, 'Wednesday'
    THURSDAY = 3, 'Thursday'
    FRIDAY = 4, 'Friday'
    SATURDAY = 5, 'Saturday'
    SUNDAY = 6, 'Sunday'


class ScheduleTemplate(models.Model):
    """
    Model representing a schedule template for a specific term and study group.

    Attributes:
        term (ForeignKey): The term associated with the schedule template.
        study_group (ForeignKey): The study group associated with the schedule
        template.
        weekday (IntegerField): The day of the week for the schedule.
        order_number (PositiveIntegerField): The order of the class
        for the day (1-10).
        subject (ForeignKey): The subject associated with the schedule template.
    """
    term = models.ForeignKey(Term, on_delete=models.CASCADE, null=False) 
    study_group = models.ForeignKey(
        StudyGroup,
        on_delete=models.CASCADE,
        null=False
    )
    weekday = models.IntegerField(choices=WeekdayChoices.choices, null=False)
    order_number = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1),      
            MaxValueValidator(10)
        ],
        null=False
    )
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=False)

    class Meta:
        """
        Metadata for ScheduleTemplate model.

        Attributes:
            ordering (list): Default ordering of the model instances.
            constraints (list): Unique constraints for the model fields.
        """
        ordering = ["term", "study_group", "weekday", "order_number"]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    'term',
                    'study_group',
                    'weekday',
                    'order_number'
                ], name='unique_schedule_template_row'
            ),
        ]

    def __str__(self):
        """
        String representation of the ScheduleTemplate instance.

        Returns:
            str: A formatted string containing the term, study group, weekday,
            order number, and subject.
        """

        return (
            f"{self.term} - "
            f"{self.study_group} - "
            f"{self.weekday} - "
            f"{self.order_number}. - "
            f"{self.subject}"
        )
