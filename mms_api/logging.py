# import logging
# from mms_api.models import LogEntry
#
#
# class DatabaseLogHandler(logging.Handler):
#     def emit(self, record):
#         try:
#             log_entry = LogEntry(
#                 action=record.getMessage(),
#             )
#             log_entry.save()
#         except Exception:
#             self.handleError(record)
