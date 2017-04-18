from django.core.urlresolvers import resolve
from django.test import TestCase

from apps.classSchedule.views import course_search_pel
from apps.classSchedule.views import course_search_res
from apps.classSchedule.views import course_search_results_pel
from apps.classSchedule.views import course_search_results_res
from apps.classSchedule.views import localsite


# Create your tests here.

class LocalsitePageTest(TestCase):
    def test_root_url_resolves_to_localsite_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, localsite)

    def test_localsite_page_uses_correct_tempalte(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'localsite.html')

    def test_course_search_pel_url_resolves_to_page_view(self):
        found = resolve('/course/search/pel/201520/R4/')
        self.assertEqual(found.func, course_search_pel)

    def test_course_search_pel_page_uses_correct_template(self):
        response = self.client.get('/course/search/pel/201525/P3/')
        self.assertTemplateUsed(response, 'course_search_pel.html')

    def test_course_search_res_url_resolves_to_page_view(self):
        found = resolve('/course/search/res/201510/R2/')
        self.assertEqual(found.func, course_search_res)

    def test_course_search_res_uses_correct_template(self):
        response = self.client.get('/course/search/res/201510/R2/')
        self.assertTemplateUsed(response, 'course_search_res.html')

    def test_course_search_results_res_url_resolves_to_page_view(self):
        found = resolve('/course/search/results/res/')
        self.assertEqual(found.func, course_search_results_res)

    def test_course_search_results_res_uses_correct_template(self):
        response = self.client.get('/course/search/results/res/')
        self.assertTemplateUsed(response, 'course_search_results_res.html')

    def test_course_search_results_pel_url_resolves_to_page_view(self):
        found = resolve('/course/search/results/pel/')
        self.assertEqual(found.func, course_search_results_pel)

    def test_course_search_results_pel_uses_correct_template(self):
        response = self.client.get('/course/search/results/pel/')
        self.assertTemplateUsed(response, 'course_search_results_pel.html')

    def test_course_search_pel_redirects_after_POST(self):
        response = self.client.post(
            '/course/search/pel/201525/P3/',
            data={
                'subject': ['0', 'All'],
                'area': ['0', 'All'],
                'instructor': ['0', 'All'],
                'specialized': ['0', 'All'],
                'campus': ['0', 'All'],
                'open_only': '0',

            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/course/search/results/pel/')

    def test_course_search_res_redirects_after_POST(self):
        response = self.client.post(
            '/course/search/res/201510/R2/',
            data={
                'subject': ['0', 'All'],
                'area': ['0', 'All'],
                'instructor': ['0', 'All'],
                'specialized': ['0', 'All'],
                'open_only': '0',

            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/course/search/results/res/')
