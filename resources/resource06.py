import simplejson as json

from twisted.internet import defer
from twisted.web import http, resource, server

from .database import HasDatabase
from .response import Response, ErrorResponse
from .resource_utils import get_user, check_content, ContentException

class DataController(HasDatabase):
    keyformat = 'data:{username}'

    def handle_POST(self, request):
        """
        @return Deferred or Failure
        """
        d = defer.succeed(request)
        d.addCallback(self._load_body)

        d.addCallback(self._merge_data, request)

        d.addCallback(lambda _: Response(200))
        return d

    @staticmethod
    def _load_body(request):
        user = get_user(request)
        body_js = request.content.read()
        content = json.loads(body_js)
        if not check_content(content):
            raise ErrorResponse(http.BAD_REQUEST, 'Illegal body')
        return content

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

class DataResource(resource.Resource):
    controller = DataController()

    def render_POST(self, request):
        """
        @return server.NOT_DONE_YET
        """
        d = defer.succeed(request)
        d.addCallback(self.controller.handle_POST)

        d.addCallback(self._render_response, request)
        d.addErrback(self._render_response_error, request)

        return server.NOT_DONE_YET

    def _render_response(self, response_obj, request):
        request.setResponseCode(response_obj.http_code)
        for header, value in response_obj.headers.items():
            request.setHeader(header, value)
        request.write(response_obj.body)
        request.finish()

    def _render_response_error(self, f, request):
        f.trap(ErrorResponse)
        response = f.value
        return _render_response(response, request)
