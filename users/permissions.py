from rest_framework import permissions

class IsModer(permissions.BasePermission):
    message = 'Вы не состоите в группе модераторы'

    def has_permission(self, request, view):
         return request.user.groups.filter(name="moders").exists()
