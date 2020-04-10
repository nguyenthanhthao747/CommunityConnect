from django.db import models

class VetCourses(models.Model):
    id = models.BigIntegerField(primary_key=True)
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
    provider_count = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'vet_courses'

class VetCoursesCategory(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'vet_courses_category'
        unique_together = (('id', 'name'),)

class VetCoursesToOccupation(models.Model):
    anzsco = models.BigIntegerField(blank=True, null=True)
    course_id = models.BigIntegerField(blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.

    class Meta:
        managed = False
        db_table = 'vet_courses_to_occupation'


class VetCoursesToProvider(models.Model):
    course_id = models.BigIntegerField(blank=True, null=True)
    campus_id = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'vet_courses_to_provider'

class CourseCategory(models.Model):
    occupation_category = models.TextField(blank=True, null=True)
    course_category = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'course_category'
