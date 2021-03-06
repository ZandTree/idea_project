from rest_framework.permissions import BasePermission

SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')


class IsAuthorOrIsStaffOrReadOnly(BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `author` attribute.
    has_object permission (for obj with id)
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        # Instance must have an attribute named `author`.       

        return bool(
            request.method in SAFE_METHODS or
            request.user and
            request.user.is_authenticated and
            not request.user.is_banned and
            (obj.author == request.user or request.user.is_staff)
        )


class IsAuthenticatedAndNotBanned(BasePermission):
    """
    Object-level permission to only allow auth-ed and not banned user
    to create an object
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        return bool(
            request.method in SAFE_METHODS or
            request.user and
            request.user.is_authenticated and
            not request.user.is_banned
        )


class IsOwnerOrIsStaff(BasePermission):
    """
    Instance must have an attribute named `user_id`.
    Only user == owner of the obj and NOT banned; OR user == staff can RUD operations on obj
    (example: profile perms)
    does NOT allow GET requests from not owner/staff
    """
   
    def has_object_permission(self, request, view, obj):
        print("inside has_obj_perms")
        print("msg from perms line 51- obj user id",obj.user_id)
        return bool(
            request.user and request.user.is_authenticated and
            not request.user.is_banned and
            (obj.user_id == request.user.id or request.user.is_staff)
        )


class IsOwnerOrIsStaffOrReadOnly(BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Others can only see content (example comments perms)
    """    

    def has_object_permission(self, request, view, obj):
        """
        Read permissions are allowed to any request,
        so we'll always allow GET, HEAD or OPTIONS requests.
        Instance must have an attribute named `user`.
        (also banned user can't edit object)
        """
        return bool(
            request.method in SAFE_METHODS or
            request.user and
            request.user.is_authenticated and
            not request.user.is_banned and
            (obj.user == request.user or request.user.is_staff)
    )

    