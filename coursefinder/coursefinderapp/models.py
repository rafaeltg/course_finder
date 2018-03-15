from django.db import models


COUNTRY_CHOICES = (
    ('XF', 'England'),
    ('XG', 'Northern Ireland'),
    ('XH', 'Scotland'),
    ('XI', 'Wales'),
)


class Location(models.Model):

    locid = models.CharField(max_length=2)
    ukprn = models.CharField(max_length=8)
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=2, choices=COUNTRY_CHOICES, default='XK')
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def __str__(self):
        return "%s" % self.name

    class Meta:
        unique_together = ('locid', 'ukprn')


class Job(models.Model):
    description = models.CharField(max_length=100)

    def __str__(self):
        return "%s" % self.description


class Course(models.Model):

    MODE_CHOICES = (
        ('1', 'Full-time'),
        ('2', 'Part-time'),
        ('3', 'Both'),
    )

    DISTANCE_CHOICES = (
        ('0', 'Course is available other than by distance learning'),
        ('1', 'Course is only available through distance learning'),
        ('2', 'Course is optionally available through distance learning'),
    )

    pubukprn = models.CharField(max_length=25)
    ukprn = models.CharField(max_length=25)
    kiscourseid = models.CharField(max_length=25)
    title = models.CharField(max_length=100)
    url = models.URLField(max_length=100)
    mode = models.CharField(max_length=1, choices=MODE_CHOICES, default='1')
    distance = models.CharField(max_length=1, choices=DISTANCE_CHOICES, default='0')
    aim = models.CharField(max_length=10)

    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True, blank=True)

    jobs = models.ManyToManyField(Job)

    def __str__(self):
        return "%s" % self.title

    class Meta:
        unique_together = ('pubukprn', 'ukprn', 'kiscourseid', 'mode')
