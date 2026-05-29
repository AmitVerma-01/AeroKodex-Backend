from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.utils import timezone
from datetime import timedelta

from users.models import User, Student
from workshops.models import WorkshopCategory, Workshop, StudentBooking

class SchoolIntegrationTestCase(APITestCase):

    def setUp(self):
        # 1. Create a Workshop Category and Workshop
        self.category = WorkshopCategory.objects.create(name="Aerospace Tech", slug="aerospace-tech")
        self.workshop = Workshop.objects.create(
            category=self.category,
            title="Introduction to Drone Fabrication",
            slug="intro-to-drone-fabrication",
            level="junior",
            description="Build your first micro-quadcopter drone from scratch.",
            duration="3 Days",
            difficulty="Beginner",
            date=timezone.now() + timedelta(days=5),
            location="AeroKodex Workshop Lab",
            price=4000.00,
            seats_available=20,
            total_seats=20,
            is_active=True
        )

        # 2. Register URLs
        self.register_url = reverse('users:register')
        self.login_url = reverse('users:login')
        self.verify_otp_url = reverse('users:verify-otp')
        self.student_list_url = "/api/auth/school/students/"
        self.booking_list_url = "/api/workshops/school/bookings/"
        self.payment_create_url = reverse('workshops:school-payment-create')
        self.payment_verify_url = reverse('workshops:school-payment-verify')

    def test_full_school_payment_flow(self):
        # Step A: Register a new school user
        reg_data = {
            "email": "school@kodex.edu",
            "username": "Kodex High School",
            "phone_number": "1234567890",
            "role": "SCHOOL",
            "password": "SecurePassword123",
            "password_confirm": "SecurePassword123"
        }
        response = self.client.post(self.register_url, reg_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['email'], reg_data['email'])

        # Fetch the created user and their OTP
        user = User.objects.get(email=reg_data['email'])
        self.assertEqual(user.role, 'SCHOOL')
        self.assertFalse(user.is_verified)
        self.assertIsNotNone(user.otp)

        # Step B: Verify the Email using OTP
        verify_data = {
            "email": user.email,
            "otp": user.otp
        }
        response = self.client.post(self.verify_otp_url, verify_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        user.refresh_from_db()
        self.assertTrue(user.is_verified)

        # Step C: Log in the user to obtain JWT tokens
        login_data = {
            "email": reg_data['email'],
            "password": reg_data['password']
        }
        response = self.client.post(self.login_url, login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        access_token = response.data['tokens']['access']

        # Authenticate the test client with JWT
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        # Step D: Add two students to the roster
        student_1_data = {
            "name": "Amit Sharma",
            "class_name": "Grade 10",
            "email": "amit@kodex.edu",
            "phone_number": "9998887776"
        }
        response = self.client.post(self.student_list_url, student_1_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        student_1_id = response.data['id']

        student_2_data = {
            "name": "Priya Verma",
            "class_name": "Grade 11",
            "email": "priya@kodex.edu",
            "phone_number": "9998887775"
        }
        response = self.client.post(self.student_list_url, student_2_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        student_2_id = response.data['id']

        # Confirm roster size is 2
        response = self.client.get(self.student_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

        # Step E: Assign both students to the drone workshop (create student bookings)
        booking_1_data = {
            "student": student_1_id,
            "workshop": self.workshop.id
        }
        response = self.client.post(self.booking_list_url, booking_1_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        booking_1_id = response.data['id']

        booking_2_data = {
            "student": student_2_id,
            "workshop": self.workshop.id
        }
        response = self.client.post(self.booking_list_url, booking_2_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        booking_2_id = response.data['id']

        # Verify bookings are both in Pending status
        response = self.client.get(self.booking_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['payment_status'], 'Pending')
        self.assertEqual(response.data[1]['payment_status'], 'Pending')

        # Step F: Initiate a Razorpay payment for both bookings
        pay_init_data = {
            "booking_ids": [booking_1_id, booking_2_id]
        }
        response = self.client.post(self.payment_create_url, pay_init_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('order_id', response.data)
        self.assertEqual(response.data['amount'], 800000)  # 2 * 4000 INR * 100 paise
        self.assertTrue(response.data['is_mock'])
        order_id = response.data['order_id']

        # Step G: Verify the simulated payment
        pay_verify_data = {
            "razorpay_order_id": order_id,
            "razorpay_payment_id": "mock_pay_1234567890",
            "razorpay_signature": "mock_sig_1234567890"
        }
        response = self.client.post(self.payment_verify_url, pay_verify_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['is_mock'])

        # Step H: Assert that bookings are updated to Paid and seats decreased
        booking_1 = StudentBooking.objects.get(id=booking_1_id)
        booking_2 = StudentBooking.objects.get(id=booking_2_id)
        self.assertEqual(booking_1.payment_status, 'Paid')
        self.assertEqual(booking_2.payment_status, 'Paid')
        self.assertEqual(booking_1.razorpay_payment_id, "mock_pay_1234567890")

        self.workshop.refresh_from_db()
        self.assertEqual(self.workshop.seats_available, 18)  # Seats decreased by 2
