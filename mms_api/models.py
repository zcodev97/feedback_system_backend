import uuid
from django.db.models import Sum
from django.conf import settings
from django.db import models, transaction
from django.db import models
from django.contrib.auth.models import User


class FeedBack(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    welcome = models.CharField(max_length=255)
    # welcome_notes = models.TextField()
    service_level = models.CharField(max_length=255)
    # service_level_notes = models.TextField()
    price_level = models.CharField(max_length=255)
    # price_level_notes = models.TextField()
    food_level = models.CharField(max_length=255)
    # food_level_notes = models.TextField()
    clean_level = models.CharField(max_length=255)
    # clean_level_notes = models.TextField()
    client_name = models.CharField(max_length=255, blank=True)
    client_number = models.CharField(max_length=255, blank=True)

    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.welcome


# class PaymentCycle(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     title = models.CharField(max_length=255)

#     def __str__(self):
#         return self.title


# class PaymentMethod(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     title = models.CharField(max_length=255)

#     def __str__(self):
#         return self.title


# class Vendor(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     vendor_id = models.CharField(max_length=255)
#     name = models.CharField(max_length=255)
#     pay_period = models.ForeignKey(PaymentCycle, on_delete=models.CASCADE)
#     pay_type = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE)
#     number = models.CharField(max_length=255, blank=True)
#     owner_name = models.CharField(max_length=255)
#     owner_phone = models.CharField(max_length=255)
#     fully_refunded = models.BooleanField()
#     penalized = models.BooleanField()
#     created_at = models.DateTimeField(auto_now=True)
#     account_manager = models.ForeignKey(
#         settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='account_manager')
#     created_by = models.ForeignKey(
#         settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

#     def __str__(self):
#         return self.name


# class Payment(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     vendor_id = models.IntegerField()
#     vendor = models.CharField(max_length=255)
#     start_date = models.DateTimeField()
#     end_date = models.DateTimeField()
#     pay_period = models.CharField(max_length=255)
#     pay_type = models.CharField(max_length=255)
#     number = models.CharField(max_length=255, blank=True)
#     to_be_paid = models.CharField(max_length=255)
#     is_paid = models.BooleanField()
#     order_count = models.JSONField()
#     orders = models.JSONField()
#     created_at = models.DateTimeField(auto_now=True)
#     created_by = models.ForeignKey(
#         settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)

#     def __str__(self):
#         return self.vendor


# class PaidOrders(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     payment_id = models.CharField(max_length=10, unique=True, editable=False)
#     order_id = models.CharField(max_length=255, unique=True)
#     order_date = models.DateTimeField()
#     vendor = models.CharField(max_length=255)
#     vendor_id = models.ForeignKey(
#         Vendor, on_delete=models.CASCADE, related_name="vendor_db_id")
#     sub_total = models.FloatField()
#     vendor_discount_cap = models.FloatField()
#     vendor_discount = models.FloatField()
#     total_discount = models.FloatField()
#     commission_percentage = models.FloatField()
#     commission_value = models.FloatField()
#     refund = models.FloatField()
#     hybrid_payment = models.FloatField()
#     to_be_paid = models.FloatField()
#     cancellation_type = models.CharField(max_length=255)
#     cancellation_reason = models.CharField(max_length=255)
#     lastStatus = models.CharField(max_length=255)
#     created_at = models.DateTimeField(auto_now=True)
#     created_by = models.ForeignKey(
#         settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

#     def generate_payment_id(self):
#         # Customize the prefix or length as needed
#         prefix = "INV"
#         # Extract 6 characters from the UUID
#         unique_id = str(uuid.uuid4().int)[:8]
#         return f"{prefix}-{unique_id}"

#     def __str__(self):
#         return self.payment_id

#     def save(self, *args, **kwargs):
#         with transaction.atomic():
#             if not self.payment_id:
#                 # Generate a short and secure invoice ID
#                 self.payment_id = self.generate_payment_id()
#             super().save(*args, **kwargs)
