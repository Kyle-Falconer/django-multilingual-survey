"""Tests for the views of the ``multilingual_survey`` app."""
from django.conf import settings
from django.test import TestCase

from django_libs.tests.factories import UserFactory
from django_libs.tests.mixins import ViewRequestFactoryTestMixin

from . import factories
from .. import views


class SurveyReportAdminViewTestCase(ViewRequestFactoryTestMixin, TestCase):
    """Tests for the ``SurveyReportAdminView`` view class."""
    view_class = views.SurveyReportAdminView

    def get_view_kwargs(self):
        return {'slug': self.survey.slug}

    def setUp(self):
        self.admin = UserFactory(is_staff=True)
        self.user = UserFactory()
        self.question = factories.SurveyQuestionFactory()
        self.survey = self.question.survey
        self.answer = factories.SurveyAnswerFactory(question=self.question)

    def test_view(self):
        self.should_redirect_to_login_when_anonymous()
        # should also redirect to login for regular users
        self.redirects(user=self.user, to='{0}?next={1}'.format(
                       settings.LOGIN_URL, self.get_url()))
        self.is_callable(user=self.admin)
        self.is_callable(user=self.admin, data={'answer': 999})
        self.is_callable(user=self.admin, data={'answer': self.answer.pk})


class SurveyReportListViewTestCase(ViewRequestFactoryTestMixin, TestCase):
    """Tests for the ``SurveyReportListView`` view class."""
    view_class = views.SurveyReportListView

    def setUp(self):
        self.admin = UserFactory(is_staff=True)
        self.user = UserFactory()
        self.survey = factories.SurveyFactory()

    def test_view(self):
        self.should_redirect_to_login_when_anonymous()
        # should also redirect to login for regular users
        self.redirects(user=self.user, to='{0}?next={1}'.format(
                       settings.LOGIN_URL, self.get_url()))
        self.is_callable(user=self.admin)


class SurveyViewTestCase(ViewRequestFactoryTestMixin, TestCase):
    """Tests for the ``SurveyView`` view class."""
    view_class = views.SurveyView

    def get_view_kwargs(self):
        return {'slug': self.survey.slug}

    def setUp(self):
        self.survey = factories.SurveyFactory()
        self.data = {}

    def test_view(self):
        self.is_callable(add_session=True)
        self.is_not_callable(kwargs={'slug': 'foo'})
        self.is_postable(add_session=True, data=self.data, ajax=True)
