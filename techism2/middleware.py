from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect
from django.contrib.auth import logout
from techism2 import service

class SecureRequiredMiddleware(object):
    
    def process_request(self, request):
        if not request.is_secure():
            # no check if no secure_url is configured
            secure_url = service.get_secure_url()
            if not secure_url.startswith("https://"):
                return None
            
            # destroy session if session cookie was submitted over non-secure connection
            if request.user.is_authenticated():
                logout(request)
                return HttpResponseRedirect('/')
            
            # redirect login page to https url
            if request.get_full_path().startswith("/accounts/"):
                url = secure_url + request.get_full_path()
                return HttpResponsePermanentRedirect(url)
        return None
