# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
from plone.dexterity.interfaces import IDexterityContent
from plone.restapi.interfaces import IExpandableElement
from plone.restapi.serializer.converters import json_compatible
from plone.restapi.services import Service
from zope.component import adapter
from zope.interface import Interface
from zope.interface import implementer


@implementer(IExpandableElement)
@adapter(IDexterityContent, Interface)
class WorkflowInfo(object):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self, expand=False):
        if not expand:
            return {'@workflow': {
                "@id": '{}/@workflow'.format(self.context.absolute_url()),
            }}

        wftool = getToolByName(self.context, 'portal_workflow')
        history = wftool.getInfoFor(self.context, "review_history")

        actions = wftool.listActionInfos(object=self.context)
        transitions = []
        for action in actions:
            if action['category'] != 'workflow':
                continue

            transitions.append({
                '@id': '{}/@workflow/{}'.format(
                    self.context.absolute_url(), action['id']),
                'title': action['title'],
            })

        return {'@workflow': {
            'history': json_compatible(history),
            'transitions': transitions,
        }}


class WorkflowInfoService(Service):
    """Get workflow information
    """
    def reply(self):
        info = WorkflowInfo(self.context, self.request)
        return info(expand=True)['@workflow']
