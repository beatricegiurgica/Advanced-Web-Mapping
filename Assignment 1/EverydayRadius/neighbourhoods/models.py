from django.contrib.gis.db import models

class PointOfInterest(models.Model):
    CATEGORY_CHOICES = [
        ('food', 'Food & Drink'),
        ('supermarket', 'Supermarket'),
        ('transport', 'Public Transport'),
        ('park', 'Park & Green Space'),
        ('shopping', 'Shopping'),
        ('school', 'School & Education'),
        ('nightlife', 'Nightlife'),
        ('health', 'Health & Pharmacy'),
    ]

    name = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, db_index=True)
    address = models.CharField(max_length=300, blank=True)
    description = models.TextField(blank=True)
    location = models.PointField(srid=4326)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Point of Interest"
        verbose_name_plural = "Points of Interest"
        ordering = ['category', 'name']
        indexes = [
            models.Index(fields=['category']),
        ]

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"

    @property
    def latitude(self):
        return self.location.y

    @property
    def longitude(self):
        return self.location.x
