import simplejson as json

from twisted.web import http, resource, server

from .database import HasDatabase
from .resource_utils import get_user, check_content

class DataResource(resource.Resource, HasDatabase):
    keyformat = 'data:{username}'

    def render_POST(self, request):
        """
        @return either None or server.NOT_DONE_YET
        @raise Exception
        """
        user = get_user(request)
        body_js = request.content.read()
        content = json.loads(body_js)
        key = self.keyformat.format(username=user.username)

        if not check_content(content):
            request.setResponseCode(http.BAD_REQUEST)
            request.write('Illegal body')
            request.finish()
            return

        d = self.database.get(key)

        def merge_results(db_data):
            for k in content:
                db_data[k] = content[k]
            return db_data

        d.addCallback(merge_results)
        d.addCallback(lambda data: self.database.write(key, data))

        d.addCallback(self._finish_request, request)

        return server.NOT_DONE_YET

    def _finish_request(self, _, request):
        request.setResponseCode(http.OK)
        request.finish()

