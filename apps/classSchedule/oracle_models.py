# django
from django.conf import settings
from django.core.cache import cache
import functools
import logging


# python
import cx_Oracle



class TimedCache(object):

    def __init__(self, time):
        self.time = time

    def __call__(self, fn, *args, **kwargs):
        """This method creates a new function from the original that utilizes the time
           set originally as the cache timer. It establishes a hash based on the function
           name and arguments to uniquely identify the hash"""

        def new_function(*args, **kwargs):
            logger = logging.getLogger("django")
            cache_name = self.create_cache_hash(fn.__name__, *args, **kwargs)
            cache_result = cache.get(cache_name)
            if cache_result is None:
                cache_result = fn(*args, **kwargs)
                cache.set(cache_name, cache_result, self.time)
                logger.debug("%s returned from Oracle with arguments %s" % (fn.__name__, args))
            else:
                logger.debug("%s returned from Cache with arguments %s" % (fn.__name__, args))
            return cache_result

        return new_function

    @staticmethod
    def create_cache_hash(name, *args, **kwargs):
        return hash(str(name) + str(args) + str(kwargs))

    def __get__(self, obj, objtype):
        """Support instance methods."""

        return functools.partial(self.__call__, obj)


class PelTerms:

    @staticmethod
    @TimedCache(21600)
    def get_pel_terms():
        """get the pel terms from banner
        displayed on localsite.html / localsite views / localsite def

        :rtype: list
        :return results - a list of tuples with all the pel term data
        """
        logger = logging.getLogger('django')
        try:
            con = cx_Oracle.Connection(settings.BANNER_CONNECTION_URL)
            cursor = con.cursor()
            query = 'SELECT TERM, PTRM, PTRM_DESC, PTRM_START, PTRM_END FROM SWVPTRM_UP_WEB'
            cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()
            con.close()
            logger.info("get_pel_term called against Oracle")
        except cx_Oracle.DatabaseError as e:
            print(e)
            results = None

        return results

    @staticmethod
    @TimedCache(21600)
    def get_selected_pel_term_desc(term, ptrm):
        """get the selected pel term
        displayed on course_search_pel.html / localsite views / course_search_pel def

        :param term:
        :param ptrm:
        :rtype: tuple
        :return: result - a tuple containing the name of the pel term
        """
        logger = logging.getLogger('django')
        try:
            con = cx_Oracle.Connection(settings.BANNER_CONNECTION_URL)
            cursor = con.cursor()
            cursor.prepare("SELECT PTRM_DESC FROM SWVPTRM_UP_WEB WHERE TERM = :the_term AND PTRM = :the_ptrm")
            cursor.execute(None, {'the_term': term, 'the_ptrm': ptrm})
            result = cursor.fetchone()
            cursor.close()
            con.close()
            logger.info("get_selected_pel_term_desc - term %s  - ptrm %s - against Oracle" % (term, ptrm))
        except cx_Oracle.DatabaseError as e:
            print(e)
            result = None
        return result


class ResTerms:

    @staticmethod
    @TimedCache(21600)
    def get_res_terms():
        """get the residential terms from banner
        displayed on localsite.html / localsite views / localsite def

        :rtype: list
        :return: results - a list of tuples with all the residential term data
        """
        logger = logging.getLogger('django')
        try:
            con = cx_Oracle.Connection(settings.BANNER_CONNECTION_URL)
            cursor = con.cursor()
            query = 'SELECT TERM, PTRM, PTRM_DESC, PTRM_START, PTRM_END FROM SWVPTRM_UR_WEB'
            cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()
            con.close()
            logger.debug("get_res_terms called against Oracle")
        except cx_Oracle.DatabaseError as e:
            print(e)
            results = None
        return results

    @staticmethod
    @TimedCache(21600)
    def get_selected_res_term_desc(term, ptrm):
        """get the selected residential term
        displayed on course_search_res.html / localsite views / course_search_res def

        :rtype: tuple
        :return: result - a tuple containing the name of the residential term
        """
        logger = logging.getLogger('django')
        try:
            con = cx_Oracle.Connection(settings.BANNER_CONNECTION_URL)
            cursor = con.cursor()
            cursor.prepare("SELECT PTRM_DESC FROM SWVPTRM_WEB WHERE TERM = :the_term AND PTRM = :the_ptrm")
            cursor.execute(None, {'the_term': term, 'the_ptrm': ptrm})
            result = cursor.fetchone()
            cursor.close()
            con.close()
            logger.debug("get_selected_res_term_desc - term %s  - ptrm %s - against Oracle" % (term, ptrm))
        except cx_Oracle.DatabaseError as e:
            print(e)
            result = None

        return result


class Subjects:

    @staticmethod
    @TimedCache(21600)
    def get_all_subjects(term='', ptrm=''):
        """get all the subjects for a term and ptrm
        displayed on course_search_res.html / localsite views / course_search_res def
        displayed on course_search_pel.html / localsite views / course_search_pel def

        :param term:
        :param ptrm:
        :rtype: list
        :return: results - a list of tuples containing all of the subjects
        """
        logger = logging.getLogger('django')
        try:
            con = cx_Oracle.Connection(settings.BANNER_CONNECTION_URL)
            cursor = con.cursor()
            cursor.prepare(
                "SELECT TERM, SUBJ, NVL(SUBJ_DESC, 'n/a'), PTRM FROM SWVSUBJ_WEB WHERE TERM = :the_term AND PTRM = :the_ptrm")
            cursor.execute(None, {'the_term': term, 'the_ptrm': ptrm})
            results = cursor.fetchall()
            cursor.close()
            con.close()
            logger.debug("get_all_subjects - term %s  - ptrm %s - against Oracle" % (term, ptrm))
        except cx_Oracle.DatabaseError as e:
            print(e)
            results = None
        return results


class PerspectiveAreas:

    @staticmethod
    @TimedCache(21600)
    def get_all_areas():
        """get all the prespective areas
        displayed on course_search_res.html / localsite views / course_search_res def
        displayed on course_search_pel.html / localsite views / course_search_pel def

        :rtype: list
        :return: results - a list of tuples containing all of the prespective areas
        """
        logger = logging.getLogger('django')
        try:
            con = cx_Oracle.Connection(settings.BANNER_CONNECTION_URL)
            cursor = con.cursor()
            query = "SELECT AREA, AREA_DESC FROM SWVAREA_PSPT_WEB"
            cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()
            con.close()
            logger.debug("get_all_areas called against Oracle")
        except cx_Oracle.DatabaseError as e:
            print(e)
            results = None
        return results


class Instructors:

    @staticmethod
    @TimedCache(21600)
    def get_all_instructors(term='', ptrm=''):
        """get all the instructors
        displayed on course_search_res.html / localsite views / course_search_res def
        displayed on course_search_pel.html / localsite views / course_search_pel def

        :param term:
        :param ptrm:
        :rtype: list
        :return: results - a list of tuples containing all of the instructors
        """
        logger = logging.getLogger('django')
        try:
            con = cx_Oracle.Connection(settings.BANNER_CONNECTION_URL)
            cursor = con.cursor()
            cursor.prepare(
                "SELECT TERM, PTRM, PREF_NAME, CA_EMAIL, PREF_FIRST_NAME, PIDM FROM SWVINST_ASGN_PTRM_WEB WHERE TERM = :the_term AND PTRM = :the_ptrm")
            cursor.execute(None, {'the_term': term, 'the_ptrm': ptrm})
            results = cursor.fetchall()
            cursor.close()
            con.close()
            logger.debug("get_all_instructors - term %s  - ptrm %s - against Oracle" % (term, ptrm))
        except cx_Oracle.DatabaseError as e:
            print(e)
            results = None
        return results


class PelSpecialized:

    @staticmethod
    @TimedCache(21600)
    def get_all_pel_specialized():
        """get all the pel specialized courses
        displayed on course_search_pel.html / localsite views / course_search_pel def

        :rtype: list
        :return: results - a list of tuples containing all of the pel specialized courses
        """
        logger = logging.getLogger('django')
        try:
            con = cx_Oracle.Connection(settings.BANNER_CONNECTION_URL)
            cursor = con.cursor()
            query = "SELECT ATTR, ATTR_DESC FROM SWVSPEC_SEARCH_WEB WHERE ATTR LIKE 'ZP%'"
            cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()
            con.close()
            logger.debug("get_all_pel_specialized called against Oracle")
        except cx_Oracle.DatabaseError as e:
            print(e)
            results = None
        return results


class ResSpecialized:

    @staticmethod
    @TimedCache(21600)
    def get_all_res_specialized():
        """get all the residential specialized courses
        displayled on course_search_res.html / localsite views / course_search_res def

        :rtype: list
        :return: results - a list of tuples containing all of the residential specialized courses
        """
        logger = logging.getLogger('django')
        try:
            con = cx_Oracle.Connection(settings.BANNER_CONNECTION_URL)
            cursor = con.cursor()
            query = "SELECT ATTR, ATTR_DESC FROM SWVSPEC_SEARCH_WEB WHERE ATTR LIKE 'ZR%'"
            cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()
            con.close()
            logger.debug("get_all_res_specialized called against Oracle")
        except cx_Oracle.DatabaseError as e:
            print(e)
            results = None
        return results


class Campus:

    @staticmethod
    @TimedCache(21600)
    def get_campus(term='', ptrm=''):
        """get the campus locations
        displayed on course_search_pel.html / localsite views / course_search_pel def

        :param term:
        :param ptrm:
        :rtype: list
        :return: results - a list of tuples containing the campus locations
        """
        logger = logging.getLogger('django')
        try:
            con = cx_Oracle.Connection(settings.BANNER_CONNECTION_URL)
            cursor = con.cursor()
            cursor.prepare(
                "SELECT TERM, PTRM, CAMP, CAMP_DESC FROM SWVCAMP_UP_WEB WHERE TERM = :the_term AND PTRM = :the_ptrm")
            cursor.execute(None, {'the_term': term, 'the_ptrm': ptrm})
            results = cursor.fetchall()
            cursor.close()
            con.close()
            logger.debug("get_campus - term %s  - ptrm %s - against Oracle" % (term, ptrm))
        except cx_Oracle.DatabaseError as e:
            print(e)
            results = None
        return results


class Section:

    @staticmethod
    @TimedCache(60)
    def get_pel_sections(term='', ptrm='', subject='', instructor='', area='', spec='', campus='', open_only=0):
        """
        displayed on course_search_results_pel.html / localsite views / course_search_results_pel def
        :param term:
        :param ptrm:
        :param subject:
        :param instructor:
        :param area:
        :param spec:
        :param campus:
        :param open_only:
         :rtype: list
        :return: results - a list containing all of the pel sections
        """
        logger = logging.getLogger('django')
        try:
            con = cx_Oracle.Connection(settings.BANNER_CONNECTION_URL)
            cursor = con.cursor()
            query = "SELECT SUBJ_DESC, CRN, SUBJ, CRSE_NUMB, SEQ_NUMB, CAMP, BILL_HRS, CRSE_TITLE, DAYS, MEET_TIME, CAPACITY, ENRL, REMAIN, INSTRUCT_ALL, DATES, LOCATION, PREREQ, TEXT, "  # 0-017
            query += "COURSE, MEET_SCHD, SESS, BN_TERM, CRSE_TEXT, CAPACITY_XLST, ENRL_XLST, REMAIN_XLST FROM SWVSECT_WEB "
            query += "WHERE INSTRUCT_PRIM = 'Y' AND TERM = '{the_term}' AND PTRM = '{the_ptrm}' ".format(
                the_term=term,
                the_ptrm=ptrm,
            )

            if subject != '0':
                query += "AND SUBJ LIKE '{the_subject}%' ".format(
                    the_subject=subject
                )

            if instructor != '0':
                query += "AND INSTRUCT_ALL LIKE '%{the_instructor}%' ".format(
                    the_instructor=instructor
                )
            if area != '0':
                query += "AND SESS = '{the_area}' ".format(
                    the_area=area
                )
            if spec != '0':
                query += "AND SPECIAL LIKE '%{the_spec}%' ".format(
                    the_spec=spec
                )

            if campus != '0':
                query += "AND CAMP = '{the_campus}' ".format(
                    the_campus=campus
                )

            if open_only != "0":
                query += "AND REMAIN > 0 "

            query += "ORDER BY SUBJ_DESC, CRSE_NUMB, SEQ_NUMB, MEET_SCHD DESC"

            cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()
            con.close()
            logger.debug("get_pel_sections - term %s - pterm %s - subject %s - instructor %s - area %s - spec %s - campus %s - open_only %s called against Oracle" % (
                term, ptrm, subject, instructor, area, spec, campus, open_only))
        except cx_Oracle.DatabaseError as e:
            print(e)
            results = None
        return results

    @staticmethod
    @TimedCache(60)
    def get_res_sections(term='', ptrm='', subject='', instructor='', area='', spec='', open_only=0):
        """
        displayed on course_search_results_res.html / localsite views / course_search_results_res def

        :param term:
        :param ptrm:
        :param subject:
        :param instructor:
        :param area:
        :param spec:
        :param open_only:
        :return: results - a list of tuples containing the residential sections
        :rtype: list
        """
        logger = logging.getLogger('django')
        try:
            con = cx_Oracle.Connection(settings.BANNER_CONNECTION_URL)
            cursor = con.cursor()
            query = "SELECT SUBJ_DESC, CRN, SUBJ, CRSE_NUMB, SEQ_NUMB, CAMP, BILL_HRS, CRSE_TITLE, DAYS, MEET_TIME, CAPACITY, ENRL, REMAIN, INSTRUCT_ALL, DATES, LOCATION, PREREQ, TEXT, "  # 0-017
            query += "COURSE, MEET_SCHD, SESS, BN_TERM, CRSE_TEXT, CAPACITY_XLST, ENRL_XLST, REMAIN_XLST FROM SWVSECT_WEB "
            query += "WHERE INSTRUCT_PRIM = 'Y' AND TERM = '{the_term}' AND PTRM = '{the_ptrm}' ".format(
                the_term=term,
                the_ptrm=ptrm,
            )

            if subject != '0':
                query += "AND SUBJ LIKE '{the_subject}%' ".format(
                    the_subject=subject
                )

            if instructor != '0':
                query += "AND INSTRUCT_ALL LIKE '%{the_instructor}%' ".format(
                    the_instructor=instructor
                )
            if area != '0':
                query += "AND SESS = '{the_area}' ".format(
                    the_area=area
                )
            if spec != '0':
                query += "AND SPECIAL LIKE '%{the_spec}%' ".format(
                    the_spec=spec
                )

            if open_only != "0":
                query += "AND REMAIN > 0 "

            query += "ORDER BY SUBJ_DESC, CRSE_NUMB, SEQ_NUMB, MEET_SCHD DESC"

            cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()
            con.close()
            logger.debug(
                ("get_res_sections - term %s - pterm %s - "
                 "subject %s - instructor %s - area %s - "
                 "spec %s - open_only %s called against Oracle") % (
                    term, ptrm, subject, instructor, area, spec, open_only))
        except cx_Oracle.DatabaseError as e:
            print(e)
            results = None
        return results
