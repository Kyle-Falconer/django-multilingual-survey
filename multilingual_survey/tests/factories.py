"""Factories for the multilingual_survey app."""
import factory

from django_libs.tests.factories import HvadFactoryMixin

from .. import models


class SurveyFactory(HvadFactoryMixin, factory.DjangoModelFactory):
    """Factory for the ``Survey`` model."""
    FACTORY_FOR = models.Survey

    language_code = 'en'
    slug = factory.Sequence(lambda n: 'slug{0}'.format(n))
    name = factory.sequence(lambda n: 'name{0}'.format(n))
