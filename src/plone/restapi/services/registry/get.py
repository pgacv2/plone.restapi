# -*- coding: utf-8 -*-
from plone.registry.interfaces import IRegistry
from plone.restapi.services import Service
from zope.component import getUtility
from zope.interface import implements
from zope.publisher.interfaces import IPublishTraverse


class RegistryGet(Service):

    implements(IPublishTraverse)

    def __init__(self, context, request):
        super(RegistryGet, self).__init__(context, request)
        self.params = []

    def publishTraverse(self, request, name):
        # Consume any path segments after /@registry as parameters
        self.params.append(name)
        return self

    @property
    def _get_record_name(self):
        if len(self.params) != 1:
            raise Exception(
                "Must supply exactly one parameter (dotted name of"
                "the record to be retrieved)")

        return self.params[0]

    def reply(self):
        registry = getUtility(IRegistry)
        value = registry[self._get_record_name]
        return value
