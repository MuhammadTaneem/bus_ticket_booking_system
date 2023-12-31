from rest_framework.permissions import BasePermission

from bus_ticket_booking.enum import UserType


class IsTicketAgentOrManagerOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        user = request.user
        # import pdb;pdb.set_trace()
        if user.is_authenticated and (user.user_type == UserType.ticket_agent or user.user_type == UserType.manager):
            return True
        return False


class IsTicketAgentOrManager(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if user.is_authenticated and (user.user_type == UserType.ticket_agent or user.user_type == UserType.manager):
            return True
        return False


class IsManager(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if user.is_authenticated and user.user_type == UserType.manager:
            return True
        return False
