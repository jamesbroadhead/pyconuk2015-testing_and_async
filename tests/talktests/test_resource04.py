from twisted.trial import unittest
from twisted.web import http, resource, server

import simplejson as json
from mock import Mock, MagicMock

from resources.resource04_get_deferred import DataResource

class TestDataResource(unittest.TestCase):
    def setUp(self):
        self.resource = DataResource()
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
        d = DataResource()._render_POST(self.mock_request)

        def make_assertions(result):
            self.assertEqual(result, None)
            self.mock_request.setResponseCode.assert_called_once_with(http.OK)
            self.mock_request.finish.assert_called_once_with()

        d.addCallback(make_assertions)
        return d
