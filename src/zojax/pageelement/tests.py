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
"""PageElement tests

$Id$
"""
import unittest, doctest
from zope import component
from zope.component.event import objectEventNotify
from zope.app.testing import setup

import element


def setUp(test):
    setup.placefulSetUp()
    setup.setUpTestAsModule(test, 'zojax.pageelement.TESTS')

    component.provideHandler(objectEventNotify)

def tearDown(test):
    setup.placefulTearDown()
    setup.tearDownTestAsModule(test)

def test_suite():
    return unittest.TestSuite((
        doctest.DocFileSuite(
            'element.txt',
            setUp=setUp, tearDown=tearDown,
            optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS,
            ),
        ))
