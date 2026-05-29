import random
import logging
from django.conf import settings
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

try:
    import razorpay
except ImportError:
    razorpay = None

from .models import StudentBooking, Workshop

logger = logging.getLogger(__name__)

class CreateRazorpayOrderView(APIView):
    """
    Creates a Razorpay Order (or Mock Order) for one or more pending student bookings.
    Request body: { "booking_ids": [1, 2, ...] }
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.role != 'SCHOOL':
            return Response(
                {"detail": "Only accounts with the School role can initiate payments for students."},
                status=status.HTTP_403_FORBIDDEN
            )

        booking_ids = request.data.get('booking_ids', [])
        if not booking_ids:
            return Response(
                {"detail": "No booking IDs provided."},
                status=status.HTTP_400_BAD_REQUEST
            )

        bookings = StudentBooking.objects.filter(
            id__in=booking_ids,
            school=request.user,
            payment_status='Pending'
        )

        if not bookings.exists():
            return Response(
                {"detail": "No matching pending bookings found for this school account."},
                status=status.HTTP_400_BAD_REQUEST
            )

        total_amount = sum(booking.price for booking in bookings)
        amount_in_paise = int(total_amount * 100)

        # Check if Razorpay keys are configured
        key_id = getattr(settings, 'RAZORPAY_KEY_ID', '')
        key_secret = getattr(settings, 'RAZORPAY_KEY_SECRET', '')

        if key_id and key_secret and razorpay:
            try:
                client = razorpay.Client(auth=(key_id, key_secret))
                order_data = {
                    'amount': amount_in_paise,
                    'currency': 'INR',
                    'receipt': f"school_receipt_{random.randint(10000, 99999)}",
                }
                order = client.order.create(data=order_data)
                order_id = order['id']
                is_mock = False
            except Exception as e:
                logger.error(f"Razorpay order creation failed: {e}")
                return Response(
                    {"detail": f"Failed to create order with Razorpay: {str(e)}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        else:
            # Fallback Mock Mode
            order_id = f"mock_order_{random.randint(100000, 999999)}"
            is_mock = True

        # Save order_id to all selected bookings
        bookings.update(razorpay_order_id=order_id)

        return Response({
            "order_id": order_id,
            "amount": amount_in_paise,
            "currency": "INR",
            "key_id": key_id if not is_mock else "mock_key",
            "is_mock": is_mock
        }, status=status.HTTP_200_OK)


class VerifyRazorpayPaymentView(APIView):
    """
    Verifies Razorpay payment signature (or mock payment) and completes the bookings.
    Request body: { "razorpay_order_id": "...", "razorpay_payment_id": "...", "razorpay_signature": "..." }
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.role != 'SCHOOL':
            return Response(
                {"detail": "Only School accounts can perform this action."},
                status=status.HTTP_403_FORBIDDEN
            )

        order_id = request.data.get('razorpay_order_id')
        payment_id = request.data.get('razorpay_payment_id')
        signature = request.data.get('razorpay_signature')

        if not order_id or not payment_id:
            return Response(
                {"detail": "Missing razorpay_order_id or razorpay_payment_id."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if this is a Mock payment
        is_mock = order_id.startswith("mock_order_") or not getattr(settings, 'RAZORPAY_KEY_ID', '')

        if not is_mock:
            # Verify via Razorpay SDK
            key_id = getattr(settings, 'RAZORPAY_KEY_ID', '')
            key_secret = getattr(settings, 'RAZORPAY_KEY_SECRET', '')
            try:
                client = razorpay.Client(auth=(key_id, key_secret))
                client.utility.verify_payment_signature({
                    'razorpay_order_id': order_id,
                    'razorpay_payment_id': payment_id,
                    'razorpay_signature': signature
                })
            except Exception as e:
                logger.warning(f"Signature verification failed: {e}")
                return Response(
                    {"detail": "Invalid payment signature verification failed."},
                    status=status.HTTP_400_BAD_REQUEST
                )

        # Retrieve and complete all bookings with this order_id
        bookings = StudentBooking.objects.filter(
            razorpay_order_id=order_id,
            school=request.user,
            payment_status='Pending'
        )

        if not bookings.exists():
            return Response(
                {"detail": "No pending bookings found for this payment transaction."},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            with transaction.atomic():
                for booking in bookings:
                    booking.payment_status = 'Paid'
                    booking.razorpay_payment_id = payment_id
                    booking.razorpay_signature = signature or "mock_signature"
                    booking.save()

                    # Decrement workshop seat
                    workshop = booking.workshop
                    if workshop.seats_available > 0:
                        workshop.seats_available -= 1
                        workshop.save(update_fields=['seats_available'])
                    else:
                        logger.warning(f"Workshop '{workshop.title}' was fully booked after payment.")
        except Exception as e:
            logger.error(f"Error completing bookings on payment success: {e}")
            return Response(
                {"detail": f"Database transaction failed: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response({
            "message": "Payment verified and bookings completed successfully.",
            "count": bookings.count(),
            "is_mock": is_mock
        }, status=status.HTTP_200_OK)
