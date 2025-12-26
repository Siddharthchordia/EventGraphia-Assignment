from django.db import models

# Create your models here.


class Event(models.Model):
    event_name = models.CharField(max_length=255)
    event_date = models.DateField()
    photographers_required = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.event_name} ({self.event_date})"


class Photographer(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Assignment(models.Model):
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='assignments',
    )
    photographer = models.ForeignKey(
        Photographer,
        on_delete=models.CASCADE,
        related_name='assignments',
    )

    class Meta:
        unique_together = ('event', 'photographer')

    def __str__(self):
        return f"{self.photographer} → {self.event}"
