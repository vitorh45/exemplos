from django.http import HttpResponse

class RequestCheckMiddleware(object):

    def process_request(self, request):
        
        try:            
            u'%s' % request.META.get('QUERY_STRING','')
        except UnicodeDecodeError:
            response = HttpResponse()
            response.status_code = 400  #Bad Request
            return response
        
        return None
