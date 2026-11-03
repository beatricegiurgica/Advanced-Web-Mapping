import json

from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.gis.geos import Point, GEOSGeometry
from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import Distance
from django.shortcuts import render

from .models import PointOfInterest
from .serializers import (POIListSerializer, POIDetailSerializer, POIGeoJSONSerializer, POICreateSerializer)


def home(request):
    return render(request, 'neighbourhoods/index.html')


# --- CRUD ---
class POIListCreateView(generics.ListCreateAPIView):
    queryset = PointOfInterest.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return POICreateSerializer
        return POIListSerializer

class POIDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PointOfInterest.objects.all()

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return POICreateSerializer
        return POIDetailSerializer


# --- SPATIAL QUERY 1: POIs within a radius ---
@api_view(['GET'])
def pois_within_radius(request):
    lat = request.query_params.get('lat')
    lon = request.query_params.get('lon')
    radius = request.query_params.get('radius', 1.0)
    category = request.query_params.get('category')

    if not lat or not lon:
        return Response(
            {'error': 'lat and lon are required.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        lat = float(lat)
        lon = float(lon)
        radius = float(radius)
    except ValueError:
        return Response(
            {'error': 'lat, lon and radius must be numbers.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    if not (-90 <= lat <= 90) or not (-180 <= lon <= 180):
        return Response(
            {'error': 'Invalid coordinates.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    center = Point(lon, lat, srid=4326)
    pois = PointOfInterest.objects.filter(
        location__distance_lte=(center, D(km=radius))
    ).annotate(
        distance=Distance('location', center)
    ).order_by('distance')

    if category:
        pois = pois.filter(category=category)

    features = []
    for poi in pois:
        features.append({
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [poi.location.x, poi.location.y],
            },
            'properties': {
                'id': poi.id,
                'name': poi.name,
                'category': poi.category,
                'category_display': poi.get_category_display(),
                'address': poi.address,
                'description': poi.description,
                'distance_m': round(poi.distance.m, 1),
            }
        })

    return Response({
        'type': 'FeatureCollection',
        'center': {'lat': lat, 'lon': lon},
        'radius_km': radius,
        'count': len(features),
        'features': features,
    })


# --- SPATIAL QUERY 2: Nearest POIs ---
@api_view(['GET'])
def nearest_pois(request):
    lat = request.query_params.get('lat')
    lon = request.query_params.get('lon')
    limit = request.query_params.get('limit', 5)
    category = request.query_params.get('category')

    if not lat or not lon:
        return Response(
            {'error': 'lat and lon are required.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        lat = float(lat)
        lon = float(lon)
        limit = int(limit)
    except ValueError:
        return Response(
            {'error': 'lat and lon must be numbers, limit must be an integer.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    center = Point(lon, lat, srid=4326)
    pois = PointOfInterest.objects.annotate(
        distance=Distance('location', center)
    ).order_by('distance')

    if category:
        pois = pois.filter(category=category)

    pois = pois[:limit]

    data = []
    for poi in pois:
        data.append({
            'id': poi.id,
            'name': poi.name,
            'category': poi.category,
            'category_display': poi.get_category_display(),
            'address': poi.address,
            'latitude': poi.location.y,
            'longitude': poi.location.x,
            'distance_m': round(poi.distance.m, 1),
        })

    return Response({
        'center': {'lat': lat, 'lon': lon},
        'count': len(data),
        'results': data,
    })


# --- SPATIAL QUERY 3: POIs within a neighbourhood polygon ---
@api_view(['POST'])
def pois_within_polygon(request):
    geojson = request.data.get('polygon')
    category = request.data.get('category')

    if not geojson:
        return Response(
            {'error': 'A GeoJSON polygon is required in the "polygon" field.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        polygon = GEOSGeometry(json.dumps(geojson), srid=4326)
    except Exception:
        return Response(
            {'error': 'Invalid GeoJSON polygon.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    pois = PointOfInterest.objects.filter(location__within=polygon)

    if category:
        pois = pois.filter(category=category)

    features = []
    for poi in pois:
        features.append({
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [poi.location.x, poi.location.y],
            },
            'properties': {
                'id': poi.id,
                'name': poi.name,
                'category': poi.category,
                'category_display': poi.get_category_display(),
                'address': poi.address,
                'description': poi.description,
            }
        })

    return Response({
        'type': 'FeatureCollection',
        'count': len(features),
        'features': features,
    })
