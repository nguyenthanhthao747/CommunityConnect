from django.db import models

class VetOccupations(models.Model):
    id = models.BigIntegerField(primary_key=True)
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


class VetProfessionsCategory(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'vet_professions_category'


class VetProfessions(models.Model):
    id = models.BigAutoField(primary_key=True)
    category_id = models.IntegerField()
    anzsco_id = models.BigIntegerField(blank=True, null=True)
    # category = models.TextField(blank=True, null=True)
    # sub_category = models.TextField(blank=True, null=True)
    # course_category = models.TextField(blank=True, null=True)
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
