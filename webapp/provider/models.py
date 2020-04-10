from django.db import models


class VetProviders(models.Model):
    id = models.BigIntegerField(primary_key=True)
    asqa_code = models.BigIntegerField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    site_name = models.TextField(blank=True, null=True)
    government_subsidised = models.TextField(blank=True, null=True)
    address_line_1 = models.TextField(blank=True, null=True)
    address_line_2 = models.TextField(blank=True, null=True)
    suburb = models.TextField(blank=True, null=True)
    postcode = models.BigIntegerField(blank=True, null=True)
    geographic_id = models.BigIntegerField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    url = models.TextField(blank=True, null=True)
    email = models.TextField(blank=True, null=True)
    is_regional = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'vet_providers'
        app_label = 'provider'


class VetGeolocations(models.Model):
    id = models.BigIntegerField(primary_key=True)
    region_name = models.TextField(blank=True, null=True)
    local_government_authority = models.TextField(blank=True, null=True)
    postcode = models.BigIntegerField(blank=True, null=True)
    location = models.TextField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'vet_geolocations'
