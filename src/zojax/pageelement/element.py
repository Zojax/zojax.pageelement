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
from zope import interface, event
from zope.location import Location
from zope.component import queryMultiAdapter, getAdapters

from interfaces import IPageElement, IPageElementView


class PageElement(Location):
    interface.implements(IPageElement)

    title = u''
    template = None
    weight = 99999
    _elements = ()

    def __init__(self, context, request, view, manager=None):
        self.__parent__ = view
        self.context = context
        self.request = request
        self.view = view
        self.manager = manager

    def update(self):
        """See zope.contentprovider.interfaces.IContentProvider"""
        # Find all content providers for the region
        context = self.context
        request = self.request
        view = self.view

        elements = []
        for name, element in getAdapters(
            (context, request, view, self), IPageElement):
            if element is not None:
                elements.append((element.weight, name, element))

        elements.sort()
        self._elements = [element for o, name, element in elements]

    @property
    def elements(self):
        for el in self._elements:
            el.update()
            if el.isAvailable():
                yield el

    def render(self):
        """See zope.contentprovider.interfaces.IContentProvider"""
        if self.template:
            return self.template()

        view = queryMultiAdapter((self, self.request), IPageElementView)
        if view is not None:
            view.update()
            return view.render()

        return u'\n'.join(
            [element.updateAndRender() for element in self._elements])

    def isAvailable(self):
        return True

    def updateAndRender(self):
        self.update()
        if self.isAvailable():
            return self.render()
        else:
            return u''
