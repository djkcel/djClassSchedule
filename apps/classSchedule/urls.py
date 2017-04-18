from django.conf.urls import url

from . import views

urlpatterns = [

    # localsite
    url(r'^$', views.localsite, {'template_name': 'localsite.html'}, name='localsite'),

    # course search pel form
    url(r'^course/search/pel/(?P<term>\d+)/(?P<ptrm>\w*)/$', views.course_search_pel,
        {'template_name': 'course_search_pel.html'}, name='course_search_pel'),

    # course search residential form
    url(r'^course/search/res/(?P<term>\d+)/(?P<ptrm>\w*)/$', views.course_search_res,
        {'template_name': 'course_search_res.html'}, name='course_search_res'),

    # course search results res
    url(r'^course/search/results/res/$', views.course_search_results_res,
        {'template_name': 'course_search_results_res.html'}, name='course_search_results_res'),

    # course search results pel
    url(r'^course/search/results/pel/$', views.course_search_results_pel,
        {'template_name': 'course_search_results_pel.html'}, name='course_search_results_pel'),

]
