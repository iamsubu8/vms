from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import *
from .serializers import *
from django.contrib.auth.models import User
from rest_framework.test import APITestCase


class UserLoginTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        # Add any necessary setup for your test, such as creating a test user.

    def test_user_login_successful(self):
        # Assuming you have a test user in your setup
        test_user_data = {
            "username": "lenovo",
            "password": "123qwe..",
        }
        response = self.client.post(reverse("user-login"), data=test_user_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertIn("token", response.data)
        # Add additional assertions based on your expected response format.

    def test_user_login_invalid_credentials(self):
        invalid_user_data = {
            "username": "lenovos",
            "password": "123qwe..",
        }
        response = self.client.post(reverse("user-login"), data=invalid_user_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)  # You may need to adjust this based on your expected behavior
        # self.assertNotIn("token", response.data)
        # Add additional assertions based on your expected response format for invalid credentials.

    def test_user_login_blank_data(self):
        blank_user_data = {
            "username": "",
            "password": "",
        }
        response = self.client.post(reverse("user-login"), data=blank_user_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)  # You may need to adjust this based on your expected behavior
        # self.assertNotIn("token", response.data)
        # Add additional assertions based on your expected response format for blank data.

    # Add more test cases as needed based on different scenarios.

class VendorViewTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.superuser = User.objects.create_superuser(username='admin', password='adminpassword', email='admin@example.com')
        # Add any necessary setup for your test, such as creating a test user.

    def test_create_vendor_successful(self):
        self.client.force_authenticate(user=self.superuser)
        test_vendor_data = {
            "name": "Test Vendor",
            "contact_details": "Test Contact",
            "address": "Test Address",
            "vender_code": "test123",
            # Add other required fields...
        }

        response = self.client.post(reverse("vendor-create"), data=test_vendor_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Vendors.objects.count(), 1)
        self.assertEqual(Vendors.objects.get().name, "Test Vendor")
        # Add additional assertions based on your expected behavior.

    # def test_create_vendor_existing_vendor_code(self):
    #     self.client.force_authenticate(user=self.superuser)
    #     # Assuming you have a vendor with vender_code 'test123' in your setup
    #     existing_vendor_data = {
    #         "name": "Test Vendor",
    #         "contact_details": "Existing Contact",
    #         "address": "Existing Address",
    #         "vender_code": "test123",
    #         # Add other required fields...
    #     }

    #     response = self.client.post(reverse("vendor-create"), data=existing_vendor_data)

    #     self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
    #     self.assertIn("this vendor already exists", response.data["msg"])
    #     # Add additional assertions based on your expected behavior for conflict.

    def test_create_vendor_blank_data(self):
        self.client.force_authenticate(user=self.superuser)
        blank_vendor_data = {
            "name": "",
            "contact_details": "",
            "address": "",
            "vender_code": "",
            # Add other required fields...
        }

        response = self.client.post(reverse("vendor-create"), data=blank_vendor_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Please fill all required fields", response.data["msg"])
        # Add additional assertions based on your expected behavior for bad request.

    def test_get_all_vendors(self):
        self.client.force_authenticate(user=self.superuser)
        # Assuming you have some vendors in your setup
        response = self.client.get(reverse("vendor-create"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue("data" in response.data)
        # Add additional assertions based on your expected behavior for retrieving all vendors.

    # # Add more test cases as needed based on different scenarios.

class VendorOperationsTestCase(APITestCase):
    def setUp(self):
        # Create a superuser for authentication
        self.superuser = User.objects.create_superuser(username='admin', password='adminpass')
        self.client.force_authenticate(user=self.superuser)

        # Create a vendor for testing
        self.vendor = Vendors.objects.create(
            name='Test Vendor',
            contact_details='Test Contact',
            address='Test Address',
            vender_code='test123'
            # Add other required fields...
        )

    def test_get_vendor_details(self):
        url = reverse('vendor-operations-detail', args=[self.vendor.id])
        self.client.force_authenticate(user=self.superuser)  # Force authentication for the client
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], True)
        self.assertEqual(response.data['data']['name'], 'Test Vendor')

    def test_update_vendor_details(self):
        self.client.force_authenticate(user=self.superuser)

        url = reverse('vendor-operations-detail', args=[self.vendor.id])
        updated_data = {
            'name': 'Updated Vendor',
            'contact_details': 'Updated Contact',
            'address': 'Updated Address',
            'vender_code': 'updated123'
            # Add other updated fields...
        }
        response = self.client.put(url, data=updated_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], True)
        self.assertEqual(response.data['msg'], 'Vendor Updated Successfully!')

        # Refresh the vendor instance from the database and check if it's updated
        self.vendor.refresh_from_db()
        self.assertEqual(self.vendor.name, 'Updated Vendor')

    def test_delete_vendor(self):
        self.client.force_authenticate(user=self.superuser)

        url = reverse('vendor-operations-detail', args=[self.vendor.id])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], True)
        self.assertEqual(response.data['msg'], 'Vendor removed Successfully!')

        # Check if the vendor is removed from the database
        with self.assertRaises(Vendors.DoesNotExist):
            Vendors.objects.get(id=self.vendor.id)


