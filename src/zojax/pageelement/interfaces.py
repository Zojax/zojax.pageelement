##############################################################################
#
# Copyright (c) 2009 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""

$Id$
"""
from zope import interface, schema
from zope.contentprovider.interfaces import IContentProvider


class IPageElement(IContentProvider):
    """ page element """

    title = schema.TextLine(
        title = u'Title',
        required = False)

    view = interface.Attribute('View')
    elements = interface.Attribute('List of page elements')

    def isAvailable():
        """ is element available """

    def updateAndRender():
        """ update and render pageelement """


class IPageElementView(interface.Interface):
    """ page element view """

    def update():
        """ update view """

    def render():
        """ render view """
