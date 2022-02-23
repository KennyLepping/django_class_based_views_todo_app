from secrets import choice
import string

from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True,
                             blank=True)  # Delete all tasks when user is deleted
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    complete = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['complete']  # Completed items will be sent to the bottom of the list


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='profile_pics/default.jpg',
                              upload_to='profile_pics/')
    login_code = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f'{self.user.username}\'s Profile'

    def generate_code(self, size=6, chars=string.ascii_uppercase + string.digits):
        self.login_code = ''.join(choice(chars) for _ in range(size))
        self.save()
