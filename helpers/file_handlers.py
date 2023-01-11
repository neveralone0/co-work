import os # rename helpers to utils later
from django.utils import timezone


def slider_image_filename_handler(instance, filename): 
    ext = filename.split('.')[-1]
    ts = timezone.now()
    filename = f'{ts.year}_{ts.month}_{ts.day}.{ext}'

    return os.path.join('sliders', filename)


def former_intern_image_filename_handler(instance, filename):
    ext = filename.split('.')[-1]
    ts = timezone.now()
    filename = f'{ts.year}_{ts.month}_{ts.day}.{ext}'

    return os.path.join('former_interns', filename)


def mentor_image_filename_handler(instance, filename):
    ext = filename.split('.')[-1]
    ts = timezone.now()
    filename = f'{ts.year}_{ts.month}_{ts.day}.{ext}'

    return os.path.join('mentors', filename)


def course_image_filename_handler(instance, filename):
    ext = filename.split('.')[-1]
    ts = timezone.now()
    filename = f'{ts.year}_{ts.month}_{ts.day}.{ext}'

    return os.path.join('courses', filename)
