from rest_framework.permissions import BasePermission

from user.constants import READ_METHODS, WRITE_METHODS


class IsAuthenticatedReadsOrAdminWrites(BasePermission):
	"""
	All Authenticated users can perform reads, Admins can perform writes
	"""

	def has_permission(self, request, view):
		if request.user and request.user.is_authenticated:
			if request.method in WRITE_METHODS:
				return True if request.user.is_staff is True else False
			return True
		return False
