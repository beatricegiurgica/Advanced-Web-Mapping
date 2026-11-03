from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from .models import PointOfInterest
from django.contrib.gis.geos import Point

class POIListSerializer(serializers.ModelSerializer):
    latitude = serializers.ReadOnlyField()
    longitude = serializers.ReadOnlyField()
    category_display = serializers.CharField(source='get_category_display', read_only=True)

    class Meta:
        model = PointOfInterest
        fields = ['id', 'name', 'category', 'category_display', 'address', 'latitude', 'longitude']

class POIDetailSerializer(serializers.ModelSerializer):
    latitude = serializers.ReadOnlyField()
    longitude = serializers.ReadOnlyField()
    category_display = serializers.CharField(source='get_category_display', read_only=True)

    class Meta:
        model = PointOfInterest
        fields = ['id', 'name', 'category', 'category_display', 'address', 'description', 'latitude', 'longitude', 'created_at', 'updated_at']

class POIGeoJSONSerializer(GeoFeatureModelSerializer):
    category_display = serializers.CharField(source='get_category_display', read_only=True)

    class Meta:
        model = PointOfInterest
        geo_field = 'location'
        fields = ['id', 'name', 'category', 'category_display', 'address', 'description']

class POICreateSerializer(serializers.ModelSerializer):
    latitude = serializers.FloatField(write_only=True)
    longitude = serializers.FloatField(write_only=True)

    class Meta:
        model = PointOfInterest
        fields = ['name', 'category', 'address', 'description', 'latitude', 'longitude']

    def validate_latitude(self, value):
        if not -90 <= value <= 90:
            raise serializers.ValidationError("Latitude must be between -90 and 90.")
        return value

    def validate_longitude(self, value):
        if not -180 <= value <= 180:
            raise serializers.ValidationError("Longitude must be between -180 and 180.")
        return value

    def validate_category(self, value):
        valid = [c[0] for c in PointOfInterest.CATEGORY_CHOICES]
        if value not in valid:
            raise serializers.ValidationError(f"Category must be one of: {', '.join(valid)}")
        return value

    def create(self, validated_data):
        latitude = validated_data.pop('latitude')
        longitude = validated_data.pop('longitude')
        validated_data['location'] = Point(longitude, latitude, srid=4326)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        latitude = validated_data.pop('latitude', None)
        longitude = validated_data.pop('longitude', None)
        if latitude is not None and longitude is not None:
            validated_data['location'] = Point(longitude, latitude, srid=4326)
        return super().update(instance, validated_data)
