from django import template
from jobosoft.models import Applicant, BookmarkJob

register = template.Library()

"""
Simple tag is used to return values and can also be used to store values for later use

register assignment_tag was removed in django 2.0
"""


@register.simple_tag
def get_number_of_applicant(job):
    # Returns the number of objects where Applicants(job)
    return Applicant.objects.filter(job=job).count()


@register.simple_tag
def is_job_already_saved(job, user):
    try:
        # Check if a user with that job exists in Bookmarks
        # if not an Error is thrown
        BookmarkJob.objects.get(job=job, user=user)
        return True
    except Exception:
        return False

@register.simple_tag
def is_job_already_applied(job, user):
    try:
        # Check if a user with that job exists in Applicant Model
        # if not an Error is thrown
        Applicant.objects.get(job=job, user=user)
        return True
    except Exception:
        return False
