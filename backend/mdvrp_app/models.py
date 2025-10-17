from django.db import models

# Create your models here.
class Customer(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)

    class Meta:
        app_label = 'mdvrp_app'