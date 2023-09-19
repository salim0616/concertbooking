from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class TestRegister(APITestCase):

    # Valid user registration
    def test_valid_user_registration(self):
        # Arrange
        request_data = {
            "email": "test@example.com",
            "password": "Password@123",
            "name":"tester1"
        }
    
        # Act
        url=reverse('register')
        response=self.client.post(url,request_data,format='json')
    
        # Assert
        assert response.status_code == status.HTTP_200_OK
        # assert response.data == "Successfully Registered"

    # Empty request data
    def test_empty_request_data(self):
        # Arrange
        request_data = {}
    
        # Act
        url=reverse('register')
        response=self.client.post(url,request_data,format='json')
    
        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        # assert response.data == {"email": ["This field is required."], "password": ["This field is required."]}

    # Minimal request data
    def test_minimal_request_data(self):
        # Arrange
        request_data = {
            "email": "test@example.com",
            "password": "password123"
        }
    
        # Act
        url=reverse('register')
        response=self.client.post(url,request_data,format='json')
    
        # Assert
        self.assertEqual(response.status_code , status.HTTP_400_BAD_REQUEST)
        

    # Invalid email format
    def test_invalid_email_format(self):
        # Arrange
        request_data = {
            "email": "invalid_email",
            "password": "password123"
        }
    
        # Act
        url=reverse('register')
        response=self.client.post(url,request_data,format='json')
    
        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        # assert response.data == {"email": ["Enter a valid email address."]}

    # Invalid password format
    def test_invalid_password_format(self):
        # Arrange
        request_data =  {
            "email": "test@example.com",
            "password": "invalid",
            "name":"tester1"
        }
    
        # Act
        url=reverse('register')
        response=self.client.post(url,request_data,format='json')
    
        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        # assert response.data == {"password": ["Password must contain at least 8 characters."]}

    # Password too short
    def test_password_too_short(self):
        # Arrange
        request_data = {
            "email": "test@example.com",
            "password": "short"
        }
    
        # Act
        url=reverse('register')
        response=self.client.post(url,request_data,format='json')
    
        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        # assert response.data == {"password": ["Password must contain at least 8 characters."]}




# import pytest

# class TestLogin:

#     # Valid email and password returns HTTP 200 and access key
#     def test_valid_email_and_password(self):
#         # Arrange
#         request = RequestFactory().post('/login', data={'email': 'valid_email@example.com', 'password': 'valid_password'})
    
#         # Act
#         response = login(request)
    
#         # Assert
#         assert response.status_code == status.HTTP_200_OK
#         assert 'access_key' in response.data

#     # Multiple successful logins generate new access keys
#     def test_multiple_successful_logins(self):
#         # Arrange
#         request = RequestFactory().post('/login', data={'email': 'valid_email@example.com', 'password': 'valid_password'})
    
#         # Act
#         response1 = login(request)
#         response2 = login(request)
    
#         # Assert
#         assert response1.data['access_key'] != response2.data['access_key']

#     # User's last login time is updated after successful login
#     def test_last_login_time_updated(self):
#         # Arrange
#         request = RequestFactory().post('/login', data={'email': 'valid_email@example.com', 'password': 'valid_password'})
    
#         # Act
#         response = login(request)
    
#         # Assert
#         user = User.objects.get(email='valid_email@example.com')
#         assert user.last_login == timezone.now()

#     # Invalid email returns HTTP 401 and error message
#     def test_invalid_email(self):
#         # Arrange
#         request = RequestFactory().post('/login', data={'email': 'invalid_email@example.com', 'password': 'valid_password'})
    
#         # Act
#         response = login(request)
    
#         # Assert
#         assert response.status_code == status.HTTP_401_UNAUTHORIZED
#         assert response.data == 'Invalid Credentials..'

#     # Invalid password returns HTTP 401 and error message
#     def test_invalid_password(self):
#         # Arrange
#         request = RequestFactory().post('/login', data={'email': 'valid_email@example.com', 'password': 'invalid_password'})
    
#         # Act
#         response = login(request)
    
#         # Assert
#         assert response.status_code == status.HTTP_401_UNAUTHORIZED
#         assert response.data == 'Invalid Credentials..'

#     # Missing email returns HTTP 400 and error message
#     def test_missing_email(self):
#         # Arrange
#         request = RequestFactory().post('/login', data={'password': 'valid_password'})
    
#         # Act
#         response = login(request)
    
#         # Assert
#         assert response.status_code == status.HTTP_400_BAD_REQUEST
#         assert response.data == 'Internal Server Error'