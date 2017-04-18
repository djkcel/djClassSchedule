"""localsite/views.py - defines the views for the localsite/landing page"""

# python
import datetime

from django.core import urlresolvers
from django.http import HttpResponseRedirect
# django
from django.shortcuts import render

from apps.classSchedule.oracle_models import Campus
from apps.classSchedule.oracle_models import Instructors
from apps.classSchedule.oracle_models import PelSpecialized
# djClassSchedulePrj
from apps.classSchedule.oracle_models import PelTerms
from apps.classSchedule.oracle_models import PerspectiveAreas
from apps.classSchedule.oracle_models import ResSpecialized
from apps.classSchedule.oracle_models import ResTerms
from apps.classSchedule.oracle_models import Section
from apps.classSchedule.oracle_models import Subjects


def localsite(request, template_name="localsite.html"):
    """localsite is the home/landing page

    query for the pel and residential terms and send them to the html template

    :param request: the request object
    :param template_name: the name of the template to use
    :return: render_to_response
    """
    pel_terms = PelTerms.get_pel_terms()
    res_terms = ResTerms.get_res_terms()
    return render(request, template_name, context=locals())


def course_search_pel(request, template_name="course_search_pel.html", term='', ptrm=''):
    """builds the course search "form" page for PEL students, which offers selectable drop down choices of subjects,
    academic area, instructor, specialized search and pel campus.

    :param request: the request object
    :param template_name: the template name to use for this view
    :param term: the pel term code
    :param ptrm: the ptrm - ex: P5
    :return: render_to_response if get request - redirect to search results if post request
    """
    if request.method == "POST":
        # write form data to session
        request.session['term'] = term
        request.session['ptrm'] = ptrm
        request.session['subject'] = str(request.POST.get('subject', ['0', 'All'])).split('|')
        request.session['area'] = str(request.POST.get('area', ['0', 'All'])).split('|')
        request.session['instructor'] = str(request.POST.get('instructor', ['0', 'All'])).split('|')
        request.session['specialized'] = str(request.POST.get('specialized', ['0', 'All'])).split('|')
        request.session['campus'] = str(request.POST.get('campus', ['0', 'All'])).split('|')
        request.session['open_only'] = request.POST.get('open_only', '0')
        return HttpResponseRedirect(urlresolvers.reverse('course_search_results_pel'))

    request.session['selected_pel_term_desc'] = selected_pel_term_desc = PelTerms().get_selected_pel_term_desc(term,
                                                                                                               ptrm)
    subjects = Subjects().get_all_subjects(term, ptrm)
    perspective_areas = PerspectiveAreas().get_all_areas()
    instructors = Instructors().get_all_instructors(term, ptrm)
    pel_specialized = PelSpecialized().get_all_pel_specialized()
    campuses = Campus().get_campus(term, ptrm)
    return render(request, template_name, context=locals())


def course_search_res(request, template_name="course_search_res.html", term='', ptrm=''):
    """builds the course search "form" page for residential students, which offers selectable drop down choices of
    subject, academic area, instructor and specialized search.

    :param request: the request object
    :param template_name: the template name to use for this view
    :param term: the residential term code
    :param ptrm: the ptrm code
    :return: render_to_response if get request - redirect to search results if post request
    """
    if request.method == "POST":
        request.session['term'] = term
        request.session['ptrm'] = ptrm
        request.session['subject'] = str(request.POST.get('subject', ['0', 'All'])).split('|')
        request.session['area'] = str(request.POST.get('area', ['0', 'All'])).split('|')
        request.session['instructor'] = str(request.POST.get('instructor', ['0', 'All'])).split('|')
        request.session['specialized'] = str(request.POST.get('specialized', ['0', 'All'])).split('|')
        request.session['open_only'] = request.POST.get('open_only', '0')
        return HttpResponseRedirect(urlresolvers.reverse('course_search_results_res'))

    request.session['selected_res_term_desc'] = selected_res_term_desc = ResTerms().get_selected_res_term_desc(term,
                                                                                                               ptrm)
    subjects = Subjects().get_all_subjects(term, ptrm)
    perspective_areas = PerspectiveAreas().get_all_areas()
    instructors = Instructors().get_all_instructors(term, ptrm)
    res_specialized = ResSpecialized().get_all_res_specialized()
    return render(request, template_name, context=locals())


def course_search_results_pel(request, template_name="course_search_results_pel.html"):
    """builds a page with PEL courses listed in a table based upon the persons selected criteria from the
    course_search_pel() method

    :param request: the request object
    :param template_name: the template to use for this view
    :return: render_to_response
    """
    year = datetime.date.today().year
    no_term = str(year) + '25'
    term = request.session.get('term', no_term)
    ptrm = request.session.get('ptrm', 'P3')
    the_subject = request.session.get('subject', ['0', 'All'])
    the_area = request.session.get('area', ['0', 'All'])
    the_instructor = request.session.get('instructor', ['0', 'All'])
    the_specialized = request.session.get('specialized', ['0', 'All'])
    the_campus = request.session.get('campus', ['0', 'All'])
    open_only = request.session.get('open_only', '0')
    selected_pel_term_desc = request.session.get('selected_pel_term_desc', 'n/a')
    sections = Section().get_pel_sections(term, ptrm, subject=the_subject[0], area=the_area[0],
                                          instructor=the_instructor[0], spec=the_specialized[0],
                                          campus=the_campus[0], open_only=open_only)
    return render(request, template_name, context=locals())


def course_search_results_res(request, template_name="course_search_results_res.html"):
    """builds a page with Residential courses listed in a table based upon the persons selected criteria from the
    course_search_res() method

    :param request: the request object
    :param template_name: the template to use for this view
    :return: render_to_response
    """
    year = datetime.date.today().year
    no_term = str(year) + '10'
    term = request.session.get('term', no_term)
    ptrm = request.session.get('ptrm', 'R2')
    default_values = ['0', 'All']
    the_subject = request.session.get('subject', default_values)
    the_area = request.session.get('area', default_values)
    the_instructor = request.session.get('instructor', default_values)
    the_specialized = request.session.get('specialized', default_values)
    open_only = request.session.get('open_only', '0')
    selected_res_term_desc = request.session.get('selected_res_term_desc', 'n/a')
    sections = Section().get_res_sections(term, ptrm, subject=the_subject[0], instructor=the_instructor[0],
                                          area=the_area[0], spec=the_specialized[0], open_only=open_only)
    return render(request, template_name, context=locals())
