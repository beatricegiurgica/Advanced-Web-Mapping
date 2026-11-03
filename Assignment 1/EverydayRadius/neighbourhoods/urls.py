from django.urls import path
from . import views

app_name = "neighbourhoods"

urlpatterns = [
    path("", views.home, name="home"),

    # CRUD
    path('api/pois/', views.POIListCreateView.as_view(), name='poi-list-create'),
    path('api/pois/<int:pk>/', views.POIDetailView.as_view(), name='poi-detail'),

    # SPATIAL QUERIES
    path('api/pois/radius/', views.pois_within_radius, name='poi-radius'),
    path('api/pois/nearest/', views.nearest_pois, name='poi-nearest'),
    path('api/pois/within-polygon/', views.pois_within_polygon, name='poi-polygon'),
]