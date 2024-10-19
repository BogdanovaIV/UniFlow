from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from terms_and_study_groups.models import StudyGroup

# Create your models here.

class UserProfile(models.Model):
    """Model representing a user profile linked to the User model.

    Attributes:
        user (OneToOneField): A unique link to a User.
        study_group (ForeignKey): Link to a StudyGroup.
        It can be null or blank.
        checked (BooleanField): Indicates if the profile has been verified;
        defaults to False.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True) 
    study_group = models.ForeignKey(
        StudyGroup,
        on_delete=models.SET_NULL,
        null=True,
        blank=True)
    checked = models.BooleanField(default=False)

    class Meta:
        ordering = ["user"]
        
    def clean(self):
        """
        Validates the UserProfile instance before saving.

        Raises:
            ValidationError: If date_from is not earlier than date_to
            or if there are overlapping terms.
        """
        # Check if checked is, StudyGroup is not empty
        if self.checked and self.study_group is None:
            raise ValidationError(
                "The study group must be filled out."
            )

    def __str__(self):
        """Return a string representation of the UserProfile."""
        return f"{self.user.username}'s Profile"