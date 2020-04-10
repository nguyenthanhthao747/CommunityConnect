# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AdminHoneypotLoginattempt(models.Model):
    username = models.CharField(max_length=255, blank=True, null=True)
    ip_address = models.CharField(max_length=39, blank=True, null=True)
    session_key = models.CharField(max_length=50, blank=True, null=True)
    user_agent = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField()
    path = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'admin_honeypot_loginattempt'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class CourseCategory(models.Model):
    occupation_category = models.TextField(blank=True, null=True)
    course_category = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'course_category'


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


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


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
    postcode = models.BigIntegerField(blank=True, null=True)
    vic_gov_region = models.TextField(blank=True, null=True)
    state = models.TextField(blank=True, null=True)
    service_name = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hospital'


class OccupationCleaned(models.Model):
    id = models.BigAutoField(primary_key=True)
    anzsco_id = models.BigIntegerField(blank=True, null=True)
    category = models.TextField(blank=True, null=True)
    sub_category = models.TextField(blank=True, null=True)
    course_category = models.TextField(blank=True, null=True)
    title = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    education = models.TextField(blank=True, null=True)
    summary = models.TextField(blank=True, null=True)
    weekly_pay = models.BigIntegerField(blank=True, null=True)
    employment_size = models.BigIntegerField(blank=True, null=True)
    future_growth = models.TextField(blank=True, null=True)
    skill_level = models.TextField(blank=True, null=True)
    unemployment = models.TextField(blank=True, null=True)
    full_time_share = models.FloatField(blank=True, null=True)
    hours = models.FloatField(blank=True, null=True)
    age = models.FloatField(blank=True, null=True)
    female = models.FloatField(blank=True, null=True)
    high_demand = models.BigIntegerField(blank=True, null=True)
    male = models.FloatField(blank=True, null=True)
    hourly_pay = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'occupation_cleaned'


class OccupationNew(models.Model):
    index = models.BigIntegerField(blank=True, null=True)
    id = models.BigIntegerField(blank=True, null=True)
    anzsco_id = models.BigIntegerField(blank=True, null=True)
    category = models.TextField(blank=True, null=True)
    sub_category = models.TextField(blank=True, null=True)
    title = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    education = models.TextField(blank=True, null=True)
    summary = models.TextField(blank=True, null=True)
    weekly_pay = models.BigIntegerField(blank=True, null=True)
    employment_size = models.TextField(blank=True, null=True)
    future_growth = models.TextField(blank=True, null=True)
    skill_level = models.TextField(blank=True, null=True)
    unemployment = models.TextField(blank=True, null=True)
    full_time_share = models.FloatField(blank=True, null=True)
    hours = models.FloatField(blank=True, null=True)
    age = models.FloatField(blank=True, null=True)
    female = models.FloatField(blank=True, null=True)
    high_demand = models.BigIntegerField(blank=True, null=True)
    male = models.FloatField(blank=True, null=True)
    hourly_pay = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'occupation_new'


class PtvStops(models.Model):
    id = models.BigIntegerField(blank=True, null=True)
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


class RentMissingMelted(models.Model):
    suburb = models.TextField(blank=True, null=True)
    postcode = models.BigIntegerField(blank=True, null=True)
    property_category = models.TextField(blank=True, null=True)
    rent_value = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'rent_missing_melted'


class RentOld(models.Model):
    suburb = models.TextField(blank=True, null=True)
    rent_1_bedroom_flat = models.BigIntegerField(blank=True, null=True)
    rent_2_bedroom_flat = models.BigIntegerField(blank=True, null=True)
    rent_3_bedroom_flat = models.BigIntegerField(blank=True, null=True)
    rent_2_bedroom_house = models.BigIntegerField(blank=True, null=True)
    rent_3_bedroom_house = models.BigIntegerField(blank=True, null=True)
    rent_4_bedroom_house = models.BigIntegerField(blank=True, null=True)
    postcode = models.BigIntegerField(blank=True, null=True)
    avg = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'rent_old'


class RentOld2(models.Model):
    suburb_id = models.IntegerField()
    suburb = models.CharField(max_length=100, blank=True, null=True)
    rent_1_bedroom_flat = models.BigIntegerField(blank=True, null=True)
    rent_2_bedroom_flat = models.BigIntegerField(blank=True, null=True)
    rent_3_bedroom_flat = models.BigIntegerField(blank=True, null=True)
    rent_2_bedroom_house = models.BigIntegerField(blank=True, null=True)
    rent_3_bedroom_house = models.BigIntegerField(blank=True, null=True)
    rent_4_bedroom_house = models.BigIntegerField(blank=True, null=True)
    postcode = models.BigIntegerField(blank=True, null=True)
    avg = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'rent_old_2'


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


class SuburbArea(models.Model):
    area_sq_m = models.FloatField(blank=True, null=True)
    suburb_id = models.BigIntegerField(blank=True, null=True)
    area_sq_km = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'suburb_area'


class SuburbBoundary(models.Model):
    suburb_id = models.IntegerField()
    name = models.TextField(blank=True, null=True)
    post_code_str = models.TextField(blank=True, null=True)
    geo_boundary = models.TextField(blank=True, null=True)
    shape_type = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'suburb_boundary'


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


class VetCourses(models.Model):
    id = models.BigAutoField(primary_key=True)
    category_id = models.IntegerField(blank=True, null=True)
    course_title = models.TextField(blank=True, null=True)
    course_code = models.TextField(blank=True, null=True)
    qualification_level = models.TextField(blank=True, null=True)
    course_type = models.TextField(blank=True, null=True)
    government_subsidised = models.BigIntegerField(blank=True, null=True)
    apprenticeship = models.BigIntegerField(blank=True, null=True)
    traineeship = models.BigIntegerField(blank=True, null=True)
    entry_requirements = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'vet_courses'


class VetCoursesCategory(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'vet_courses_category'
        unique_together = (('id', 'name'),)


class VetCoursesToOccupation(models.Model):
    anzsco = models.BigIntegerField(blank=True, null=True)
    course_id = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'vet_courses_to_occupation'


class VetCoursesToProvider(models.Model):
    course_id = models.BigIntegerField(blank=True, null=True)
    campus_id = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'vet_courses_to_provider'


class VetGeolocations(models.Model):
    id = models.BigAutoField(primary_key=True)
    region_name = models.TextField(blank=True, null=True)
    local_government_authority = models.TextField(blank=True, null=True)
    postcode = models.BigIntegerField(blank=True, null=True)
    location = models.TextField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'vet_geolocations'


class VetOccupations(models.Model):
    id = models.BigAutoField(primary_key=True)
    anzsco_id = models.BigIntegerField(blank=True, null=True)
    title = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    education = models.TextField(blank=True, null=True)
    summary = models.TextField(blank=True, null=True)
    weekly_pay = models.BigIntegerField(blank=True, null=True)
    employment_size = models.TextField(blank=True, null=True)
    future_growth = models.TextField(blank=True, null=True)
    skill_level = models.TextField(blank=True, null=True)
    unemployment = models.TextField(blank=True, null=True)
    full_time_share = models.FloatField(blank=True, null=True)
    hours = models.FloatField(blank=True, null=True)
    age = models.FloatField(blank=True, null=True)
    female = models.FloatField(blank=True, null=True)
    high_demand = models.BigIntegerField(blank=True, null=True)
    male = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'vet_occupations'


class VetProfessions(models.Model):
    id = models.BigAutoField(primary_key=True)
    category_id = models.IntegerField()
    anzsco_id = models.BigIntegerField(blank=True, null=True)
    category = models.TextField(blank=True, null=True)
    sub_category = models.TextField(blank=True, null=True)
    course_category = models.TextField(blank=True, null=True)
    title = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    education = models.TextField(blank=True, null=True)
    summary = models.TextField(blank=True, null=True)
    weekly_pay = models.BigIntegerField(blank=True, null=True)
    employment_size = models.BigIntegerField(blank=True, null=True)
    future_growth = models.TextField(blank=True, null=True)
    skill_level = models.TextField(blank=True, null=True)
    unemployment = models.TextField(blank=True, null=True)
    full_time_share = models.FloatField(blank=True, null=True)
    hours = models.FloatField(blank=True, null=True)
    age = models.FloatField(blank=True, null=True)
    female = models.FloatField(blank=True, null=True)
    high_demand = models.BigIntegerField(blank=True, null=True)
    male = models.FloatField(blank=True, null=True)
    hourly_pay = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'vet_professions'


class VetProfessionsCategory(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'vet_professions_category'
        unique_together = (('id', 'name'),)


class VetProviders(models.Model):
    id = models.BigAutoField(primary_key=True)
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
