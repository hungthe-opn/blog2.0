from rest_framework.response import Response
from django.http import JsonResponse
from apps.user.models import CreateUserModel


# class MiddlewareRole:
#     def __init__(self, get_response):
#         self.get_response = get_response
#
#     def __call__(self, request):
#         if request.user.is_authenticated:
#             if CreateUserModel.objects.filter(id=request.user.id).exists():
#                 user = CreateUserModel.objects.filter(id=request.user.id).first()
#                 if user.is_author:
#                     if user.is_admin:
#                         role = 'admin'
#                     else:
#                         role = 'author'
#                 else:
#                     role = 'user'
#             else:
#                 return JsonResponse({
#                     'message': 'Error Invalid Role'
#                 })
#
#             return role
#
#         return self.get_response(request)
