# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


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


class VetCourses(models.Model):
    id = models.BigIntegerField(blank=True, null=True)
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


class VetCoursesToOccupation(models.Model):
    anzsco = models.BigIntegerField(blank=True, null=True)
    course_id = models.BigIntegerField(db_column='Course ID', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.

    class Meta:
        managed = False
        db_table = 'vet_courses_to_occupation'


class VetCoursesToProvider(models.Model):
    course_id = models.BigIntegerField(blank=True, null=True)
    campus_id = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'vet_courses_to_provider'


class VetDemo(models.Model):
    id = models.BigIntegerField(blank=True, null=True)
    anzsco_id = models.BigIntegerField(blank=True, null=True)
    title = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    education = models.TextField(blank=True, null=True)
    summary = models.TextField(blank=True, null=True)
    weekly_pay = models.TextField(blank=True, null=True)
    employment_size = models.BigIntegerField(blank=True, null=True)
    future_growth = models.TextField(blank=True, null=True)
    skill_level = models.TextField(blank=True, null=True)
    unemployment = models.TextField(blank=True, null=True)
    full_time_share = models.TextField(blank=True, null=True)
    hours = models.TextField(blank=True, null=True)
    age = models.TextField(blank=True, null=True)
    gender = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'vet_demo'


class VetGeolocations(models.Model):
    id = models.BigIntegerField(blank=True, null=True)
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
    id = models.BigIntegerField(blank=True, null=True)
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


class VetProviders(models.Model):
    id = models.BigIntegerField(blank=True, null=True)
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
