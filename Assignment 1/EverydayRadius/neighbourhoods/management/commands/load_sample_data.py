from django.core.management.base import BaseCommand
from django.contrib.gis.geos import Point
from neighbourhoods.models import PointOfInterest

SAMPLE_POIS = [
    # --- Dublin ---
    ("Tesco Express Dame Street", "supermarket", "Dame Street, Dublin 2", 53.3442, -6.2617),
    ("Dunnes Stores St Stephen's Green", "supermarket", "St Stephen's Green, Dublin 2", 53.3402, -6.2631),
    ("The Hairy Lemon", "food", "Lower Stephen Street, Dublin 2", 53.3413, -6.2637),
    ("Bewley's Grafton Street", "food", "Grafton Street, Dublin 2", 53.3418, -6.2603),
    ("St Stephen's Green Park", "park", "St Stephen's Green, Dublin 2", 53.3382, -6.2591),
    ("Merrion Square Park", "park", "Merrion Square, Dublin 2", 53.3394, -6.2494),
    ("Luas St Stephen's Green", "transport", "St Stephen's Green, Dublin 2", 53.3392, -6.2612),
    ("Pearse DART Station", "transport", "Westland Row, Dublin 2", 53.3435, -6.2479),
    ("Brown Thomas", "shopping", "Grafton Street, Dublin 2", 53.3425, -6.2600),
    ("Penneys O'Connell Street", "shopping", "O'Connell Street, Dublin 1", 53.3489, -6.2608),
    ("Trinity College Dublin", "school", "College Green, Dublin 2", 53.3438, -6.2546),
    ("University College Dublin", "school", "Belfield, Dublin 4", 53.3099, -6.2215),
    ("Dicey's Garden", "nightlife", "Harcourt Street, Dublin 2", 53.3359, -6.2635),
    ("The Grand Social", "nightlife", "Lower Liffey Street, Dublin 1", 53.3470, -6.2634),
    ("Boots Grafton Street", "health", "Grafton Street, Dublin 2", 53.3426, -6.2593),
    ("City Pharmacy Dame Street", "health", "Dame Street, Dublin 2", 53.3441, -6.2655),

    # --- Cork ---
    ("Dunnes Stores Cork", "supermarket", "St Patrick's Street, Cork", 51.8992, -8.4717),
    ("Tesco Extra Cork", "supermarket", "Merchant's Quay, Cork", 51.9001, -8.4680),
    ("Nash 19", "food", "Princes Street, Cork", 51.8971, -8.4728),
    ("The English Market", "food", "Grand Parade, Cork", 51.8980, -8.4750),
    ("Fitzgerald's Park", "park", "Mardyke, Cork", 51.8964, -8.4959),
    ("Páirc Uí Chaoimh", "park", "Marina Park, Cork", 51.8993, -8.4348),
    ("Cork Kent Station", "transport", "Lower Glanmire Road, Cork", 51.9019, -8.4580),
    ("Cork Bus Station", "transport", "Parnell Place, Cork", 51.8999, -8.4664),
    ("Brown Thomas Cork", "shopping", "St Patrick's Street, Cork", 51.8990, -8.4707),
    ("Mahon Point Shopping Centre", "shopping", "Mahon, Cork", 51.8851, -8.3966),
    ("University College Cork", "school", "Western Road, Cork", 51.8937, -8.4920),
    ("Cork Institute of Technology", "school", "Rossa Avenue, Cork", 51.8861, -8.5335),
    ("Cyprus Avenue", "nightlife", "Caroline Street, Cork", 51.8985, -8.4698),
    ("The Crane Lane", "nightlife", "Phoenix Street, Cork", 51.8979, -8.4697),
    ("Boots Cork", "health", "St Patrick's Street, Cork", 51.8986, -8.4746),
    ("Cork University Hospital Pharmacy", "health", "Wilton, Cork", 51.8831, -8.5124),

    # --- Galway ---
    ("Tesco Galway", "supermarket", "Headford Road, Galway", 53.2802, -9.0479),
    ("Dunnes Stores Galway", "supermarket", "Eyre Square, Galway", 53.2732, -9.0506),
    ("Ard Bia at Nimmos", "food", "Spanish Arch, Galway", 53.2697, -9.0537),
    ("McDonagh's Fish & Chips", "food", "Quay Street, Galway", 53.2710, -9.0543),
    ("Eyre Square Park", "park", "Eyre Square, Galway", 53.2744, -9.0492),
    ("Salthill Promenade", "park", "Salthill, Galway", 53.2578, -9.0870),
    ("Galway Bus Station", "transport", "Eyre Square, Galway", 53.2737, -9.0465),
    ("Galway Train Station", "transport", "Eyre Square, Galway", 53.2736, -9.0470),
    ("Eyre Square Shopping Centre", "shopping", "Eyre Square, Galway", 53.2731, -9.0504),
    ("Galway Shopping Centre", "shopping", "Headford Road, Galway", 53.2803, -9.0478),
    ("NUI Galway", "school", "University Road, Galway", 53.2799, -9.0608),
    ("Galway Technical Institute", "school", "Dublin Road, Galway", 53.2677, -9.0592),
    ("University of Galway", "school", "University Road, Galway", 53.2800, -9.0610),
    ("The Roisin Dubh", "nightlife", "Dominick Street, Galway", 53.2702, -9.0582),
    ("Garavan's Bar", "nightlife", "William Street, Galway", 53.2734, -9.0520),
    ("Boots Galway", "health", "Eyre Square, Galway", 53.2730, -9.0527),
    ("University College Hospital Galway", "health", "Newcastle Road, Galway", 53.2772, -9.0668),

    # --- Limerick ---
    ("Dunnes Stores Limerick", "supermarket", "Sarsfield Street, Limerick", 52.6653, -8.6302),
    ("Tesco Limerick", "supermarket", "Childers Road, Limerick", 52.6489, -8.6204),
    ("The Locke Bar", "food", "George's Quay, Limerick", 52.6641, -8.6244),
    ("Hook & Ladder", "food", "Sarsfield Street, Limerick", 52.6652, -8.6294),
    ("People's Park", "park", "Pery Square, Limerick", 52.6625, -8.6222),
    ("University of Limerick Campus Park", "park", "Castletroy, Limerick", 52.6742, -8.5718),
    ("Limerick Colbert Station", "transport", "Parnell Street, Limerick", 52.6597, -8.6314),
    ("Limerick Bus Station", "transport", "Parnell Street, Limerick", 52.6600, -8.6318),
    ("Cruises Street Shopping", "shopping", "Cruises Street, Limerick", 52.6648, -8.6278),
    ("Parkway Shopping Centre", "shopping", "Dublin Road, Limerick", 52.6712, -8.5956),
    ("University of Limerick", "school", "Castletroy, Limerick", 52.6748, -8.5718),
    ("Limerick Institute of Technology", "school", "Moylish, Limerick", 52.6827, -8.6063),
    ("Dolan's Warehouse", "nightlife", "Dock Road, Limerick", 52.6588, -8.6368),
    ("The Strand Bar", "nightlife", "Lower Shannon Street, Limerick", 52.6629, -8.6258),
    ("Boots Limerick", "health", "Cruises Street, Limerick", 52.6647, -8.6275),
    ("Barringtons Hospital Pharmacy", "health", "George's Quay, Limerick", 52.6638, -8.6242),

    # --- Waterford ---
    ("Dunnes Stores Waterford", "supermarket", "City Square, Waterford", 52.2581, -7.1121),
    ("Tesco Waterford", "supermarket", "Ardkeen, Waterford", 52.2511, -7.0838),
    ("The Granville Hotel Bar", "food", "The Quay, Waterford", 52.2592, -7.1097),
    ("Kazbar", "food", "Arundel Square, Waterford", 52.2584, -7.1127),
    ("People's Park Waterford", "park", "The Mall, Waterford", 52.2597, -7.1088),
    ("Waterford Greenway", "park", "Bilberry, Waterford", 52.2628, -7.0947),
    ("Waterford Bus Station", "transport", "The Quay, Waterford", 52.2594, -7.1104),
    ("Waterford Train Station", "transport", "Dock Road, Waterford", 52.2578, -7.1042),
    ("City Square Shopping Centre", "shopping", "Barronstand Street, Waterford", 52.2583, -7.1118),
    ("Waterford Retail Park", "shopping", "Bilberry, Waterford", 52.2642, -7.0895),
    ("Waterford Institute of Technology", "school", "Cork Road, Waterford", 52.2441, -7.1197),
    ("De La Salle College", "school", "Newtown Road, Waterford", 52.2528, -7.0982),
    ("The Munster Bar", "nightlife", "Bailey's New Street, Waterford", 52.2588, -7.1108),
    ("The Pulpit Bar", "nightlife", "Barronstrand Street, Waterford", 52.2582, -7.1122),
    ("Boots Waterford", "health", "City Square, Waterford", 52.2580, -7.1119),
    ("University Hospital Waterford Pharmacy", "health", "Dunmore Road, Waterford", 52.2467, -7.0894),
]

class Command(BaseCommand):
    help = 'Load sample Points of Interest for Ireland cities'

    def handle(self, *args, **kwargs):
        if PointOfInterest.objects.exists():
            self.stdout.write(self.style.WARNING('Sample data already exists. Skipping.'))
            return

        created = 0
        for name, category, address, lat, lon in SAMPLE_POIS:
            PointOfInterest.objects.create(
                name=name,
                category=category,
                address=address,
                location=Point(lon, lat, srid=4326),
            )
            created += 1

        self.stdout.write(self.style.SUCCESS(f'Successfully loaded {created} points of interest.'))
