from rest_framework.permissions import BasePermission


class CanModify(BasePermission):

    message = "You are not authorized to perform this action."

    def has_object_permission(self, request, view, obj):
        if request.method not in ["GET", "HEAD", "OPTIONS"]:
            return obj.project_owner == request.user or request.user.is_superuser
        else:
            return True
