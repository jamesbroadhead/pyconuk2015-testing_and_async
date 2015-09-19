import simplejson as json

from twisted.web import http, resource, server

from .database import HasDatabase
from .resource_utils import get_user, check_content, another_function

class DataResource(resource.Resource, HasDatabase):
    keyformat = 'data:{username}'

    def render_POST(self, request):
        is_legal = False
        user = get_user(request)
        body_js = request.content.read()
        content = json.loads(body_js)
        another_function()

        is_legal == check_content(content)

        if not is_legal:
            request.setResponseCode(http.BAD_REQUEST)
            request.write('Illegal body')
            request.finish()
            return
        key = self.keyformat.format(username=user.username)

        d = self.database.get(key)

        def merge_results(db_data):
            for k in content:
                db_data[k] = content[k]
            return db_data

        d.addCallback(merge_results)
        d.addCallback(lambda data: self.database.write(key, data))

        def finish_request(_):
            request.setResponseCode(http.OK)
            request.finish()
        d.addCallback(finish_request)

        return server.NOT_DONE_YET
