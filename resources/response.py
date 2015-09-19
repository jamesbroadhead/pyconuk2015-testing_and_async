
class Response(object):
    """ value object representing a http response """
    body = ''
    headers = {}

    def __init__(self, http_code, body=None, headers=None):
        self.http_code = http_code
      
        if body is not None:
            self.body = body         
        if headers is not None:
            self.headers = headers

    def __eq__(self, other):
        return (type(self) == type(other) and
                self.http_code == other.http_code and
                self.body == other.body and
                self.headers == other.headers)

    def __ne__(self, other):
        return not self == other

class ErrorResponse(Exception, Response):
    """ value object representing a http error response """
    def __init__(self, http_code, body=None, headers=None):
        Exception.__init__(self, http_code)
        Response.__init__(self, http_code, 
                          body=body, headers=headers)
