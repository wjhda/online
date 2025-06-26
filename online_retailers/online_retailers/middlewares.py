import json
from django.utils.deprecation import MiddlewareMixin
import rest_framework

class AppendCodeToResponseMiddleware(MiddlewareMixin):

    def append_code_to_response(self, response):
        result = {}
        result['code'] = response.status_code
        result['msg'] = response.status_text
        result['data'] = response.data
        response.content = json.dumps(result)
        response.data = result
        return response

    def process_response(self, request, response):
        if isinstance(response, rest_framework.response.Response):
            return self.append_code_to_response(response)
        return response
