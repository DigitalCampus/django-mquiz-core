# mquiz/api/auth.py
from tastypie.authentication import Authentication
from tastypie.authorization import Authorization

class MquizAPIAuthentication(Authentication):
    def is_authenticated(self, request, **kwargs):
        if 'alex' in request.user.username:
            return True
        return False

    # Optional but recommended
    def get_identifier(self, request):
        return request.user.username

class MquizAPIAuthorization(Authorization):
    def is_authorized(self, request, object=None):
        return True

    # Optional but useful for advanced limiting, such as per user.
    def apply_limits(self, request, object_list):
        if request and hasattr(request, 'user'):
            return object_list.filter(username=request.user.username)

        return object_list.none()
    
