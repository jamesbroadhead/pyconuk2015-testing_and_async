import simplejson as json

from twisted.internet import defer
from twisted.web import http, resource, server

from .database import HasDatabase
from .resource_utils import get_user, check_content

class DataResource(resource.Resource, HasDatabase):
    keyformat = 'data:{username}'

    def render_POST(self, request):
        """
        @return server.NOT_DONE_YET
        """
        d = defer.succeed(request)
        d.addCallback(self._render_POST)
        return server.NOT_DONE_YET

    def _render_POST(self, request):
        """
        @return None or a Deferred
        @raise Exception
        """
        user = get_user(request)
        body_js = request.content.read()
        content = json.loads(body_js)

        if not check_content(content):
            request.setResponseCode(http.BAD_REQUEST)
            request.write('Illegal body')
            request.finish()
            return

        d = self._merge_data(content, user.username)
        d.addCallback(self._finish_request, request)
        return d

    def _finish_request(self, _, request):
        request.setResponseCode(http.OK)
        request.finish()

    def _merge_data(self, content, username):
        keyformat = 'data:{username}'
        key = keyformat.format(username=username)

        d = self.database.get(key)
        d.addCallback(self._merge_results, content)
        d.addCallback(lambda data: self.database.write(key, data))
        return d

    @staticmethod
    def _merge_results(db_data, content):
        for k in content:
            db_data[k] = content[k]
        return db_data
