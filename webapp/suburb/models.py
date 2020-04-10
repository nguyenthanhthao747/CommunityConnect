from django.db import models

class Suburb(models.Model):
    id = models.BigAutoField(primary_key=True)
    region_name = models.TextField(blank=True, null=True)
    lga = models.TextField(blank=True, null=True)
    postcode = models.CharField(max_length=20, blank=True, null=True)
    suburb = models.TextField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    is_regional = models.BigIntegerField(blank=True, null=True)
    area_sq_m = models.FloatField(blank=True, null=True)
    area_sq_km = models.FloatField(blank=True, null=True)
    connectivity_index = models.FloatField()

    class Meta:
        managed = False
        db_table = 'suburb'

class SuburbInfo(models.Model):
    id = models.BigIntegerField(primary_key=True)
    suburb = models.TextField(blank=True, null=True)
    distance_from_cbd = models.FloatField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    no_of_incidents = models.BigIntegerField(blank=True, null=True)
    population = models.BigIntegerField(blank=True, null=True)
    crate = models.FloatField(blank=True, null=True)
    crime_star = models.FloatField(blank=True, null=True)
    area_sq_km = models.FloatField(blank=True, null=True)
    stops_count = models.BigIntegerField(blank=True, null=True)
    provider_count = models.BigIntegerField(blank=True, null=True)
    school_count = models.BigIntegerField(blank=True, null=True)
    hospital_count = models.BigIntegerField(blank=True, null=True)
    connectivity_index = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'suburb_info'

class SuburbBoundary(models.Model):
    suburb_id = models.IntegerField()
    name = models.TextField(blank=True, null=True)
    post_code_str = models.TextField(blank=True, null=True)
    geo_boundary = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'suburb_boundary'


class Rents(models.Model):
    suburb_id = models.IntegerField()
    suburb = models.TextField(blank=True, null=True)
    avg = models.BigIntegerField(blank=True, null=True)
    postcode = models.TextField(blank=True, null=True)
    property_category = models.TextField(blank=True, null=True)
    rent_value = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'rents'


class School(models.Model):
    suburb_id = models.IntegerField()
    education_sector = models.TextField(blank=True, null=True)
    entity_type = models.BigIntegerField(blank=True, null=True)
    school_no = models.BigIntegerField(blank=True, null=True)
    school_name = models.TextField(blank=True, null=True)
    school_type = models.TextField(blank=True, null=True)
    school_status = models.TextField(blank=True, null=True)
    address_town = models.TextField(blank=True, null=True)
    address_state = models.TextField(blank=True, null=True)
    address_postcode = models.BigIntegerField(blank=True, null=True)
    postal_town = models.TextField(blank=True, null=True)
    postal_state = models.TextField(blank=True, null=True)
    postal_postcode = models.BigIntegerField(blank=True, null=True)
    full_phone_no = models.TextField(blank=True, null=True)
    lga_id = models.BigIntegerField(blank=True, null=True)
    lga_name = models.TextField(blank=True, null=True)
    x = models.FloatField(blank=True, null=True)
    y = models.FloatField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    postal_address = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'school'


class Hospital(models.Model):
    suburb_id = models.IntegerField()
    longitude = models.FloatField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    f_id = models.BigIntegerField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    ops_name = models.TextField(blank=True, null=True)
    type = models.TextField(blank=True, null=True)
    street_num = models.TextField(blank=True, null=True)
    road_name = models.TextField(blank=True, null=True)
    road_type = models.TextField(blank=True, null=True)
    road_suffix = models.TextField(blank=True, null=True)
    campus_code = models.BigIntegerField(blank=True, null=True)
    lga = models.TextField(blank=True, null=True)
    locality_na = models.TextField(blank=True, null=True)
    postcode = models.CharField(max_length=20, blank=True, null=True)
    vic_gov_region = models.TextField(blank=True, null=True)
    state = models.TextField(blank=True, null=True)
    service_name = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hospital'


class PtvStops(models.Model):
    id = models.BigIntegerField(primary_key=True)
    suburb_id = models.IntegerField()
    stop_name = models.TextField(blank=True, null=True)
    lat = models.FloatField(blank=True, null=True)
    lng = models.FloatField(blank=True, null=True)
    routes_using_stop = models.TextField(blank=True, null=True)
    geo_boundary = models.TextField(blank=True, null=True)
    suburb = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ptv_stops'


class CrimeRate(models.Model):
    suburb_id = models.IntegerField()
    postcode = models.TextField(blank=True, null=True)
    no_of_incidents = models.BigIntegerField(blank=True, null=True)
    population = models.BigIntegerField(blank=True, null=True)
    crime_rate = models.FloatField(blank=True, null=True)
    crime_star = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'crime_rate'
