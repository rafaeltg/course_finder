import csv
import os
from django.core.management.base import BaseCommand
from coursefinderapp.models import Location, Course, Job


class Command(BaseCommand):

    def handle(self, *args, **options):
        self.load_locations()
        self.load_courses()
        self.load_jobs()

    def load_locations(self):
        """
        Load location data from LOCATION.csv
        """

        print('>> Loading Locations...')

        Location.objects.all().delete()

        def handler(line):
            """
            Translate each line of the csv file in a Location object.
            :param line: csv line
            :return: Location object
            """

            loc = Location(
                locid=line[3] if len(line[3]) == 2 else '0'+line[3],
                ukprn=line[0],
                name=line[4],
                country=line[9],
                latitude=float(line[6]) if line[6] != '' else None,
                longitude=float(line[7]) if line[7] != '' else None,
            )
            return loc

        locs = self._read_csv('/coursefinderapp/data/LOCATION.csv', handler=handler)
        Location.objects.bulk_create(locs)

    def load_courses(self):
        """
        Load courses data from KISCOURSE.csv
        Replace AIMCODE by AIMLABEL using data from KISAIM.csv
        """

        print('>> Loading Courses...')

        Course.objects.all().delete()

        # Load Course AIM Labels
        aim_label = {}

        with open(os.getcwd() + '/coursefinderapp/data/KISAIM.csv') as f:
            next(f)  # Skip the header
            reader = csv.reader(f, skipinitialspace=True)
            aim_label = dict(reader)

        course_locs = self.load_course_locations()

        def handler(line):
            """
            Translate each line of the csv in a Course object and associate with the
            its respective location.
            :param line: csv line
            :return: Course object
            """

            c = Course(
                pubukprn=line[0],
                ukprn=line[1],
                kiscourseid=line[14],
                title=line[27].replace('"', ""),
                url=line[4],
                distance=line[6],
                mode=line[15],
                aim=aim_label[line[32]],
            )

            loc_id = course_locs.get((c.pubukprn, c.ukprn, c.kiscourseid, c.mode), None)

            if loc_id is not None:
                c.location = Location.objects.get(ukprn=c.ukprn, locid=loc_id)

            return c

        courses = self._read_csv('/coursefinderapp/data/KISCOURSE.csv', handler=handler)
        Course.objects.bulk_create(courses)

    def load_course_locations(self):
        """
        Load location data from COURSELOCATION.csv
        """

        def handler(line):
            return ((line[0], line[1], line[2], line[3]), line[4]) if len(line[4]) > 0 else None

        course_locs = self._read_csv('/coursefinderapp/data/COURSELOCATION.csv', handler=handler)
        return dict(course_locs)

    def load_jobs(self):
        """
        Load jobs data from JOBLIST.csv and associate with courses
        :return:
        """

        print('>> Loading Jobs...')

        Job.objects.all().delete()

        found_jobs = {}
        courses_jobs = {}

        def handler(line):
            """
            Translate each line of the csv file in a Job object.
            :param line: csv line
            """

            job_desc = line[5].title()

            job = found_jobs.get(job_desc, None)
            if job is None:
                job = Job(description=job_desc)
                job.save()
                found_jobs[job_desc] = job

            course_key = (line[0], line[1], line[2], line[3])
            course_jobs = courses_jobs.get(course_key, [])
            course_jobs.append(job)
            courses_jobs[course_key] = course_jobs

            return None

        self._read_csv('/coursefinderapp/data/JOBLIST.csv', handler=handler)

        for c_key, jobs in courses_jobs.items():
            c = Course.objects.get(
                pubukprn=c_key[0],
                ukprn=c_key[1],
                kiscourseid=c_key[2],
                mode=c_key[3],
            )
            c.jobs.add(*jobs)

    @staticmethod
    def _read_csv(file='', handler=None):
        obj_list = []

        with open(os.getcwd() + file) as f:
            reader = csv.reader(f)
            next(reader)  # skip header

            for l in reader:
                obj = handler(l)
                if obj is not None:
                    obj_list.append(obj)

        return obj_list
