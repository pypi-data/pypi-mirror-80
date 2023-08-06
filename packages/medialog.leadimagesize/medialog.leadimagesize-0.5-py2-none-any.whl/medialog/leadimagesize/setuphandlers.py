# -*- coding: utf-8 -*-
from Products.CMFPlone.interfaces import INonInstallable
from zope.interface import implementer
from zope.interface import noLongerProvides, alsoProvides
from medialog.leadimagesize.interfaces import ILeadImageSizeSettings
from medialog.controlpanel.interfaces import IMedialogControlpanelSettingsProvider


def post_install(context):
    """Post install script"""
    # Do something at the end of the installation of this package.
    alsoProvides(ILeadImageSizeSettings, IMedialogControlpanelSettingsProvider)

def uninstall(context):
    """Uninstall script"""
    # Do something at the end of the uninstallation of this package.
    noLongerProvides(ILeadImageSizeSettings, IMedialogControlpanelSettingsProvider)
