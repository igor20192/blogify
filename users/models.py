from django.db import models
from django.contrib.auth.models import User
from django.db import models
from PIL import Image


class Profile(models.Model):
    """User Profile Model.

    Attributes:
    - user: A one-to-one relationship to the User model.
    - avatar: Field for uploading a profile picture.

    Methods:
    - __str__: Returns a string representation of the Profile object.
    - save: Overridden method to save the Profile object while resizing the uploaded image.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(default="avatars/default.jpg", upload_to="avatars")

    def __str__(self):
        """Returns a string representation of the Profile object.

        Returns:
        - A string containing the username and the word "Profile"."""
        return f"{self.user.username} Profile"

    def save(self, *args, **kwargs):
        """Overridden method to save a Profile object with resizing the loaded image.

        Parameters:
        - *args: Position arguments.
        - **kwargs: Named arguments."""
        super().save(*args, **kwargs)
        img = Image.open(self.avatar.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.avatar.path)
