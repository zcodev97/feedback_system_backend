# from .models import EndpointLog
#
# class LoggingMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response
#
#     def determine_action(self, path, method):
#         # Define your logic here to determine the action based on the path and method
#         # For example:
#         if path.startswith('/api/users/') and method == 'POST':
#             return 'create_user'
#         # Add more conditions as needed
#         return 'unknown_action'
#
#     def __call__(self, request):
#         user = request.user if request.user.is_authenticated else None
#         action = self.determine_action(request.path, request.method)
#
#         log_entry = EndpointLog(
#             user=user,
#             path=request.path,
#             method=request.method,
#             action=action,
#         )
#
#         response = self.get_response(request)
#
#         log_entry.status_code = response.status_code
#         log_entry.save()
#
#         return response
