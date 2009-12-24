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
import os.path
from zope import interface, schema
from zope.component.zcml import adapter
from zope.security.checker import defineChecker, Checker, CheckerPublic
from zope.configuration.fields import Path, Tokens, MessageID
from zope.configuration.fields import GlobalObject, GlobalInterface
from zope.configuration.exceptions import ConfigurationError
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from z3c.pt.pagetemplate import ViewPageTemplateFile

from element import PageElement
from interfaces import IPageElement


class IPageElementDirective(interface.Interface):
    """A directive to register a new page element. """

    name = schema.TextLine(
        title = u"The name of the page element.",
        description = u"The name shows up in URLs/paths. For example 'foo'.",
        required = True)

    for_ = GlobalObject(
        title = u"Context",
        description = u"The content interface or class this pagelet is for.",
        default = interface.Interface,
        required = False)

    view = GlobalObject(
        title = u'View',
        description = u'The view for which the layout should be available',
        default = interface.Interface,
        required = False)

    layer = GlobalObject(
        title = u'Layer',
        description = u'The layer for which the element should be available',
        required = False,
        default = IDefaultBrowserLayer)

    class_ = GlobalObject(
        title=u"Class",
        description=u"A class that provides attributes used by the page element.",
        required=False)

    manager = GlobalObject(
        title=u"Manager",
        description=u"A parent page element.",
        required=False)

    template = Path(
        title = u'Page element template.',
        description = u"Refers to a file containing a page template (should " \
                                      "end in extension ``.pt`` or ``.html``).",
        required=False)

    provides = GlobalInterface(
        title=u"Interface the layout provides",
        description=u"This attribute specifies the interface the layout"
                      " instance will provide.",
        default = IPageElement,
        required=False)

    title = MessageID(
        title = u'Title',
        required = False)

    description = MessageID(
        title = u'Description',
        required = False)


# Arbitrary keys and values are allowed to be passed to the pagelet.
IPageElementDirective.setTaggedValue('keyword_arguments', True)

managers = {}


def pageelementDirective(
    _context, name, for_ = interface.Interface,
    view = interface.Interface, layer = IDefaultBrowserLayer,
    manager = None, class_ = None, template=u'', provides = IPageElement,
    title=u'', description=u'', weight=9999, **kwargs):

    # Make sure that the template exists
    if template:
        template = os.path.abspath(str(_context.path(template)))
        if not os.path.isfile(template):
            raise ConfigurationError("No such file", template)

    # Build a new class that we can use different permission settings if we
    # use the class more then once.
    cdict = dict(kwargs)
    cdict['__name__'] = name
    cdict['title'] = title
    cdict['description'] = description

    try:
        weight = int(weight)
    except:
        weight = 999999

    cdict['weight'] = weight

    if template:
        cdict['template'] = ViewPageTemplateFile(template)

    if class_ is None:
        bases = (PageElement,)
    else:
        bases = (class_, PageElement)

    newclass = type(str('<PageElement %s>'%name), bases, cdict)

    # Set up permission mapping for various accessible attributes
    required = {}

    for iface in (provides, IPageElement):
        for iname in iface:
            required[iname] = CheckerPublic

    required = {'__call__': CheckerPublic,
                'browserDefault': CheckerPublic,
                'publishTraverse': CheckerPublic}

    # provide the custom provides interface if not allready provided
    if not provides.implementedBy(newclass):
        interface.classImplements(newclass, provides)

    # security checker
    defineChecker(newclass, Checker(required))

    # managers
    managers[name] = newclass

    # register the page element
    adapter(_context, (newclass,), provides, (for_, layer, view), name=name)

    if manager is not None:
        # register page element as adapter with manager
        adapter(_context,
                (newclass,), provides, (for_, layer, view, manager), name=name)


class IIncludePageElementDirective(interface.Interface):
    """A directive to register a new page element. """

    name = schema.TextLine(
        title = u"The name of the page element.",
        description = u"The name shows up in URLs/paths. For example 'foo'.",
        required = True)

    layer = GlobalObject(
        title = u'Layer',
        description = u'The layer for which the element should be available',
        required = False,
        default = IDefaultBrowserLayer)

    manager = GlobalObject(
        title=u"Manager",
        description=u"A parent page element.",
        required=False)
