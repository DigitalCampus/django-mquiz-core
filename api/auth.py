# mquiz/api/auth.py
from tastypie.authorization import Authorization

class MquizAPIAuthorization(Authorization):
    def is_authorized(self, request, object=None):
        return True

    # Optional but useful for advanced limiting, such as per user.
    def apply_limits(self, request, object_list):
        if request and hasattr(request, 'user'):
            return object_list.filter(username=request.user.username)

        return object_list.none()