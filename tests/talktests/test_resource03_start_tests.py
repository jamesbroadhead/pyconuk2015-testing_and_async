from twisted.trial import unittest
from twisted.web import http, server

import simplejson as json
from mock import MagicMock

from resources.resource03_start_tests import DataResource

class TestDataResource(unittest.TestCase):

    def test_side_effects(self):
        request = MagicMock()
        request.content.read.return_value = json.dumps(
            {'hi': 'foo'})

        self.assertEqual(
                DataResource().render_POST(request),
                server.NOT_DONE_YET)

        # wait for the deferred to resolve :-/
        request.setResponseCode.assert_called_once_with(
            http.OK)
        request.finish.assert_called_once_with()

    # ... more tests
