

# -*- coding: utf-8 -*-
from __future__ import absolute_import
from Acquisition import aq_inner
from plone import schema
from plone.app.portlets.portlets import base
from plone.memoize.instance import memoize
from plone.portlets.interfaces import IPortletDataProvider
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from z3c.form import field
from zope.component import getMultiAdapter
from zope.interface import implementer
from plone import api

import json
import six.moves.urllib.request, six.moves.urllib.parse, six.moves.urllib.error
import six.moves.urllib.request, six.moves.urllib.error, six.moves.urllib.parse


class ILeadimagePortlet(IPortletDataProvider):
    image_size = schema.Choice(
        default="preview",
        vocabulary='medialog.leadimagesize.LeadImageSizeVocabulary',
        defaultFactory=lambda: api.portal.get_registry_record('medialog.leadimagesize.interfaces.ILeadImageSizeSettings.leadsize') ,
    )


@implementer(ILeadimagePortlet)
class Assignment(base.Assignment):
    schema = ILeadimagePortlet

    def __init__(self, image_size='preview'):
        self.image_size = image_size


    @property
    def title(self):
        return 'Lead Image'


class AddForm(base.AddForm):
    schema = ILeadimagePortlet
    form_fields = field.Fields(ILeadimagePortlet)
    label = (u'Add Lead Image')
    description = (u'This portlet displays the lead image.')

    def create(self, data):
        return Assignment(
            image_size=data.get('image_size', 'preview'),
        )


class EditForm(base.EditForm):
    schema = ILeadimagePortlet
    form_fields = field.Fields(ILeadimagePortlet)
    label = (u'Edit Lead Image portlet')
    description = (u'This portlet displays the lead image.')


class Renderer(base.Renderer):
    schema = ILeadimagePortlet
    _template = ViewPageTemplateFile('leadimage.pt')

    def __init__(self, *args):
        base.Renderer.__init__(self, *args)
        context = aq_inner(self.context)
        portal_state = getMultiAdapter(
            (context, self.request),
            name=u'plone_portal_state'
        )
        self.anonymous = portal_state.anonymous()

    def render(self):
        return self._template()

    @property
    def available(self):
        """Show the portlet only if there are one or more elements and
        not an anonymous user."""
        return self.context.image

    def image_size(self):
        return self['image_size']
