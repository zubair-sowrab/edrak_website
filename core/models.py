from django.db import models
from django.utils.translation import gettext_lazy as _

class Project(models.Model):
    STATUS_CHOICES = (
        ('ready', _('Ready to Move')),
        ('off_plan', _('Off-Plan Investment')),
        ('commercial', _('Commercial Hub')),
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ready')
    image = models.ImageField(upload_to='projects/', blank=True, null=True, help_text="Main Cover Image")
    map_embed_code = models.TextField(blank=True, help_text="Paste Google Maps <iframe> code here")
    total_flats = models.IntegerField(default=0)
    parking_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class ProjectImage(models.Model):
    project = models.ForeignKey(Project, related_name='gallery', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='projects/gallery/')

class ProjectFeature(models.Model):
    project = models.ForeignKey(Project, related_name='features', on_delete=models.CASCADE)
    feature = models.CharField(max_length=200)

class Lease(models.Model):
    PROPERTY_TYPES = (
        ('apartment', _('Apartment')),
        ('villa', _('Luxury Villa')),
        ('commercial', _('Commercial Space')),
        ('townhouse', _('Townhouse')),
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True, related_name='leases')
    property_type = models.CharField(max_length=50, choices=PROPERTY_TYPES)
    location = models.CharField(max_length=200)
    rent_price = models.DecimalField(max_digits=12, decimal_places=2)
    bedrooms = models.IntegerField(default=0)
    bathrooms = models.IntegerField(default=0)
    size_sqft = models.IntegerField(default=0)
    image = models.ImageField(upload_to='leases/', blank=True, null=True, help_text="Main Cover Image")
    map_embed_code = models.TextField(blank=True, help_text="Paste Google Maps <iframe> code here")
    parking_available = models.BooleanField(default=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class LeaseImage(models.Model):
    lease = models.ForeignKey(Lease, related_name='gallery', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='leases/gallery/')

class LeaseFeature(models.Model):
    lease = models.ForeignKey(Lease, related_name='features', on_delete=models.CASCADE)
    feature = models.CharField(max_length=200)

class Inquiry(models.Model):
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=50)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False, help_text="Mark as True once you have contacted the client.")
    admin_note = models.TextField(blank=True, help_text="Internal notes for the admin.") # <-- Add this line

    def __str__(self):
        return f"Inquiry from {self.name} - {self.phone}"