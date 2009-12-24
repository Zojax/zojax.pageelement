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
"""pageelement tales expression registrations

$Id$
"""
import logging, sys
from zope import event, interface
from zope.component import queryMultiAdapter
from zope.tales.expressions import StringExpr
from zope.contentprovider.interfaces import BeforeUpdateEvent

from chameleon.core import types
from chameleon.zpt import expressions

from interfaces import IPageElement


class PageelementExpression(object):

    def __call__(self, context, request, view, name):
        # Try to look up the provider.
        pageelement = queryMultiAdapter(
            (context, request, view), IPageElement, name)

        # if the provider was not found return empty string
        if pageelement is None:
            log = logging.getLogger('zojax.pageelement')
            log.warning('Page Element "%s" is not found.'%name)
            return u''

        # Render the HTML content.
        try:
            return pageelement.updateAndRender()
        except Exception, exc:
            log = logging.getLogger('zojax.pageelement')
            log.warning(u'Error: ' + unicode(exc), exc_info=True)
            return unicode(exc)


class TALESPageelementExpression(StringExpr, PageelementExpression):

    def __call__(self, econtext):
        name = StringExpr.__call__(self, econtext)

        context = econtext.vars['context']
        request = econtext.vars['request']
        view = econtext.vars['view']

        return PageelementExpression.__call__(self,context,request,view,name)


class PageelementTranslator(expressions.ExpressionTranslator):

    symbol = '_get_zojax_pageelement'
    pageelement_traverser = PageelementExpression()

    def translate(self, string, escape=None):
        value = types.value("%s(context, request, view, '%s')" % \
                                (self.symbol, string))
        value.symbol_mapping[self.symbol] = self.pageelement_traverser
        return value
