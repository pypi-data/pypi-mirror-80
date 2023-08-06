from plone.app.contenttypes.behaviors.viewlets import LeadImageViewlet
from zope.interface import implements, Interface
#from Products.Five import BrowserView
#from zope import schema

import Acquisition
from zope.component import getUtility, getMultiAdapter
from medialog.leadimagesize.portlets.leadimage import ILeadimagePortlet
from plone.portlets.interfaces import IPortletRetriever, IPortletManager

class LeadImageViewlet(LeadImageViewlet):
    """ Viewlet """

    def has_portlet(self):
        for column in ["plone.leftcolumn", "plone.rightcolumn"]:
            manager = getUtility(IPortletManager, name=column)
            retriever = getMultiAdapter((self.context, manager), IPortletRetriever)
            portlets = retriever.getPortlets()

            for portlet in portlets:
                if ILeadimagePortlet.providedBy(portlet["assignment"]):
                    return True

        return False
