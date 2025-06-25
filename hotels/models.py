from django.db import models
from django.contrib.auth import get_user_model
from config.model_utils.models import TimeStampedModel 
from django.core.validators import MaxValueValidator

User = get_user_model()


class Hotel(models.Model):
    name = models.CharField(max_length=255)
    lat = models.FloatField()
    lon = models.FloatField()
    city = models.CharField(max_length=100)
    address = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    stars = models.IntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)



class FavoriteHotel(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="favorites")
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name="favorited_by")

    class Meta:
        unique_together = ['user', 'hotel']  

    def __str__(self):
        return f"{self.user} - {self.hotel.name}"
    


class Review(TimeStampedModel, models.Model):
    hotel = models.ForeignKey('hotels.Hotel', related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey('users.User', related_name='reviews', on_delete=models.SET_NULL, null=True, blank=True)
    content = models.TextField()
    rating = models.PositiveIntegerField(validators=[MaxValueValidator(5)])

    
    def __str__(self):
        return f"review by : {self.user.username}"
    

