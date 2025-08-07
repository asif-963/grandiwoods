from django.db import models
from django.utils.timezone import now
from ckeditor.fields import RichTextField
from django.utils import timezone


# Create your models here.
class ContactModel(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    message = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name if self.name else "Unnamed Contact"

class NearByPlace(models.Model):
    name = models.CharField(max_length=200,blank=True, null=True)
    description = models.TextField()
    image = models.ImageField(upload_to='Place_images/',blank=True, null=True)
    created_date = models.DateTimeField(default=now,blank=True, null=True)

    def __str__(self):
        return self.name

# Client Reviews
class ClientReview(models.Model):
    client_name = models.CharField(max_length=100, null=True, blank=True)
    client_image = models.ImageField(upload_to='client_images/', null=True, blank=True)
    designation = models.CharField(max_length=100, null=True, blank=True)
    review = models.TextField(null=True, blank=True)
    def __str__(self):
        return f"{self.client_name} - {self.designation}"


        
# add Folders 
class Folder(models.Model):
    name = models.CharField(max_length=100,null=True,blank=True)

    def __str__(self):
        return self.name

class Gallery(models.Model):
    folder = models.ForeignKey(Folder, related_name='galleries', on_delete=models.CASCADE)
    # description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.folder.name} - {self.description[:50]}"

class GalleryImage(models.Model):
    gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='gallery_images/')

    def __str__(self):
        return f"Image for {self.gallery.folder}"



class Booking(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=15)
    arrival_date = models.DateField(blank=True, null=True)
    departure_date = models.DateField(blank=True, null=True)
    adults = models.IntegerField(blank=True, null=True)
    children = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"Booking for {self.name} from {self.arrival_date} to {self.departure_date}"




class RoomPrice(models.Model):
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2, help_text="Regular price per night")
    offer_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Offer price per night")

    def __str__(self):
        return f"Room (Price: ₹{self.price_per_night}, Offer: ₹{self.offer_price or 'N/A'})"

class ChatMessage(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# Guest 
class Guest(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='guests/')
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

