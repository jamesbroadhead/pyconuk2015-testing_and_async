import simplejson as json

from twisted.internet import defer
from twisted.web import http, resource, server

from .database import HasDatabase
from .resource_utils import get_user, check_content, ContentException

class DataResource5(resource.Resource, HasDatabase):
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
        @return Deferred or Failure
        """
        d = defer.succeed(request)
        d.addCallback(self._load_body)
        d.addCallback(self._merge_data, request)
        d.addCallback(self._finish_request, request)

        d.addErrback(self._finish_request_on_error, request)
        return d

    def _finish_request(self, _, request):
        request.setResponseCode(http.OK)
        request.finish()

    @staticmethod
    def _load_body(request):
        body_js = request.content.read()
        content = json.loads(body_js)
        if not check_content(content):
            raise ContentException(content)
        return content

    def _finish_request_on_error(self, f, request):
        f.trap(ContentException)
        request.setResponseCode(http.BAD_REQUEST)
        request.write('Illegal body')
        request.finish()

    def _merge_data(self, content, request):
        user = get_user(request)

        keyformat = 'data:{username}'
        key = keyformat.format(username=user.username)

        d = self.database.get(key)
        d.addCallback(self._merge_results, content)
        d.addCallback(lambda data: self.database.write(key, data))
        return d

    @staticmethod
    def _merge_results(db_data, content):
        for k in content:
            db_data[k] = content[k]
        return db_data
