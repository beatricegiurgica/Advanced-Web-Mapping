from django.contrib.gis import admin
from django.contrib.gis.forms import OSMWidget
from .models import PointOfInterest


@admin.register(PointOfInterest)
class PointOfInterestAdmin(admin.GISModelAdmin):
    list_display = ['name', 'category', 'address', 'created_at']
    list_filter = ['category']
    search_fields = ['name', 'address']
    ordering = ['category', 'name']
    gis_widget = OSMWidget
