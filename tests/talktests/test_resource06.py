from __future__ import print_function

from twisted.internet import defer
from twisted.python.failure import Failure
from twisted.trial import unittest
from twisted.web import http, resource, server

import simplejson as json
from mock import Mock, MagicMock

from resources.resource06 import DataResource, DataController
from resources.resource_utils import dmockfunc as stub_success
from resources.resource_utils import fmockfunc as stub_failure
from resources.response import Response, ErrorResponse

from resources.resource_utils import ContentException


class TestDataResource(unittest.TestCase):
    def setUp(self):
        self.resource = DataResource()
        self.mock_request = MagicMock()
        self.mock_request.content.read.return_value = json.dumps({'hi': 'foo'})


    def test_render_POST_hands_over(self):
        """ test that render_POST hands off to _render_POST """
        request = MagicMock()
        self.resource.controller.handle_POST = Mock(return_value=Response(200))

        self.assertEqual(
                self.resource.render_POST(request),
                server.NOT_DONE_YET)

        self.resource.controller.handle_POST.assert_called_once_with(request)

    def test_render_POST_does_not_raise(self):
        def raise_exc(*args):
            raise Exception()
        self.resource._render_POST = raise_exc

        self.assertEqual(
                self.resource.render_POST(Mock()),
                server.NOT_DONE_YET)

        self.flushLoggedErrors(Exception)

    def test_inner_method(self):
        d = DataController().handle_POST(self.mock_request)
        d.addCallback(self.assertEqual, Response(200))
        return d


class TestControlFlow(unittest.TestCase):

    def setUp(self):
        self.controller = DataController()

    def test_load_body_fails(self):
        exc = ErrorResponse(401)
        expected = defer.fail(exc).result
        sentinel = object()

        self.controller._load_body = stub_failure(exc)
        self.controller._merge_data = stub_success(None)
        self.controller._finish_request = stub_success(None)
        self.controller._finish_request_on_error = stub_success(sentinel)

        request = object()

        d = self.controller.handle_POST(request)
        d.addErrback(lambda f: f.value)
        d.addCallback(self.assertEqual, exc)

        d.addCallback(lambda _: self.flushLoggedErrors(ErrorResponse))
        return d
