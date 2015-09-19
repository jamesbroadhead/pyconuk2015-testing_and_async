from __future__ import print_function

from twisted.trial import unittest
from twisted.web import http, server

import simplejson as json
from mock import Mock, MagicMock

from resources.resource05_controller import DataResource5
from resources.resource_utils import dmockfunc as stub_success
from resources.resource_utils import fmockfunc as stub_failure
from resources.resource_utils import ContentException


class TestDataResource(unittest.TestCase):
    def setUp(self):
        self.resource = DataResource5()
        self.mock_request = MagicMock()
        self.mock_request.content.read.return_value = json.dumps({'hi': 'foo'})


    def test_render_POST_hands_over(self):
        """ test that render_POST hands off to _render_POST """
        request = object()
        self.resource._render_POST = Mock()

        self.assertEqual(
                self.resource.render_POST(request),
                server.NOT_DONE_YET)

        self.resource._render_POST.assert_called_once_with(request)

    def test_render_POST_does_not_raise(self):
        def raise_exc(*args):
            raise Exception()
        self.resource._render_POST = raise_exc

        self.assertEqual(
                self.resource.render_POST(Mock()),
                server.NOT_DONE_YET)

        self.flushLoggedErrors(Exception)

    def test_inner_method(self):
        d = DataResource5()._render_POST(self.mock_request)

        def make_assertions(result):
            self.assertEqual(result, None)
            self.mock_request.setResponseCode.assert_called_once_with(http.OK)
            self.mock_request.finish.assert_called_once_with()

        d.addCallback(make_assertions)
        return d


class TestControlFlow(unittest.TestCase):

    def setUp(self):
        self.resource = DataResource5()

    def test_load_body_fails(self):
        exc = ContentException('hi')
        sentinel = object()

        self.resource._load_body = stub_failure(exc)
        self.resource._merge_data = stub_success(None)
        self.resource._finish_request = stub_success(None)
        self.resource._finish_request_on_error = stub_success(sentinel)

        request = object()

        d = self.resource._render_POST(request)
        d.addCallback(self.assertEqual, sentinel)
        d.addCallback(lambda _: self.flushLoggedErrors(ContentException))
        return d
